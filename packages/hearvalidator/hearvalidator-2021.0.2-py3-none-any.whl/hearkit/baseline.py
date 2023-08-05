"""
Baseline model for HEAR 2021 NeurIPS competition.

This is simply a mel spectrogram followed by random projection.
"""

import math
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Optional, Tuple

import librosa
import torch
import torch.nn.functional as F
from torch import Tensor


class RandomProjectionMelEmbedding(torch.nn.Module):
    n_fft = 4096
    n_mels = 256
    sample_rate = 44100
    seed = 0
    epsilon = 1e-4

    def __init__(self):
        super().__init__()
        torch.random.manual_seed(self.seed)

        # Create a Hann window buffer to apply to frames prior to FFT.
        self.register_buffer("window", torch.hann_window(self.n_fft))

        # Create a mel filter buffer.
        mel_scale: Tensor = torch.tensor(
            librosa.filters.mel(self.sample_rate, n_fft=self.n_fft, n_mels=self.n_mels)
        )
        self.register_buffer("mel_scale", mel_scale)

        # Projection matrices.
        normalization = math.sqrt(self.n_mels)
        self.emb4096 = torch.nn.Parameter(torch.rand(self.n_mels, 4096) / normalization)
        self.emb2048 = torch.nn.Parameter(torch.rand(self.n_mels, 2048) / normalization)
        self.emb512 = torch.nn.Parameter(torch.rand(self.n_mels, 512) / normalization)
        self.emb128 = torch.nn.Parameter(torch.rand(self.n_mels, 128) / normalization)
        self.emb20 = torch.nn.Parameter(torch.rand(self.n_mels, 20) / normalization)

        # An activation to squash the 20D embedding to a [0, 1] range.
        self.activation = torch.nn.Sigmoid()

    def forward(self, x: Tensor):
        # Compute the real-valued Fourier transform on windowed input signal.
        x = torch.fft.rfft(x * self.window)

        # Convert to a power spectrum.
        x = torch.abs(x) ** 2.0

        # Apply the mel-scale filter to the power spectrum.
        x = torch.matmul(x, self.mel_scale.transpose(0, 1))

        # Convert to a log mel spectrum.
        x = torch.log(x + self.epsilon)

        # Apply projections to get all required embeddings
        x4096 = x.matmul(self.emb4096)
        x2048 = x.matmul(self.emb2048)
        x512 = x.matmul(self.emb512)
        x128 = x.matmul(self.emb128)
        x20 = x.matmul(self.emb20)

        # The 20-dimensional embedding is specified to be int8. To cast to int8 we'll
        # apply an activation to ensure the embedding is in a 0 to 1 range first.
        x20 = self.activation(x20)

        # Scale to int8 value range and cast to int
        int8_max = torch.iinfo(torch.int8).max
        int8_min = torch.iinfo(torch.int8).min
        x20 = x20 * (int8_max - int8_min) + int8_min
        x20 = x20.type(torch.int8)

        return {4096: x4096, 2048: x2048, 512: x512, 128: x128, 20: x20}


def input_sample_rate() -> int:
    """
    Returns:
        One of the following values: [16000, 22050, 44100, 48000].
            To avoid resampling on-the-fly, we will query your model
            to find out what sample rate audio to provide it.
    """
    return RandomProjectionMelEmbedding.sample_rate


def load_model(model_file_path: str, device: str = "cpu") -> Any:
    """
    In this baseline, we don't load anything from disk.

    Args:
        model_file_path: Load model checkpoint from this file path.
            device: For inference on machines with multiple GPUs,
            this instructs the participant which device to use. If
            “cpu”, the CPU should be used (Multi-GPU support is not
            required).
    Returns:
        Model
    """
    return RandomProjectionMelEmbedding().to(device)


def frame_audio(
    audio: Tensor, frame_size: int, frame_rate: float, sample_rate: int
) -> Tuple[Tensor, Tensor]:
    """
    Slices input audio into frames that are centered and occur every
    sample_rate / frame_rate samples. If sample_rate is not divisible
    by frame_rate, we round to the nearest sample.

    Args:
            audio: input audio, expects a 2d Tensor of shape:
            (batch_size, num_samples)
        frame_size: the number of samples each resulting frame should be
        frame_rate: number of frames per second of audio
        sample_rate: sampling rate of the input audio

    Returns:
        - A Tensor of shape (batch_size, num_frames, frame_size)
        - A 1d Tensor of timestamps corresponding to the frame
        centers.
    """
    audio = F.pad(audio, (frame_size // 2, frame_size - frame_size // 2))
    num_padded_samples = audio.shape[1]

    frame_number = 0
    frames = []
    timestamps = []
    frame_start = 0
    frame_end = frame_size
    while True:
        frames.append(audio[:, frame_start:frame_end])
        timestamps.append(frame_number / frame_rate)

        # Increment the frame_number and break the loop if the next frame end
        # will extend past the end of the padded audio samples
        frame_number += 1
        frame_start = int(round(sample_rate * frame_number / frame_rate))
        frame_end = frame_start + frame_size

        if not frame_end <= num_padded_samples:
            break

    return torch.stack(frames, dim=1), torch.tensor(timestamps)


def get_audio_embedding(
    audio: Tensor,
    model: RandomProjectionMelEmbedding,
    frame_rate: float,
    batch_size: Optional[int] = 512,
) -> Tuple[Dict[int, Tensor], Tensor]:
    """
    Args:
        audio: n_sounds x n_samples of mono audio in the range
            [-1, 1]. We are making the simplifying assumption that
            for every task, all sounds will be padded/trimmed to
            the same length. This doesn’t preclude people from
            using the API for corpora of variable-length sounds;
            merely we don’t implement that as a core feature. It
            could be a wrapper function added later.
        model: Loaded model, in PyTorch or Tensorflow 2.x. This
            should be moved to the device the audio tensor is on.
        frame_rate: Number of embeddings that the model should return
            per second. Embeddings and the corresponding timestamps should
            start at 0s and increment by 1/frame_rate seconds. For example,
            if the audio is 1.1s and the frame_rate is 4.0, then we should
            return embeddings centered at 0.0s, 0.25s, 0.5s, 0.75s and 1.0s.
        batch_size: The participants are responsible for estimating
            the batch_size that will achieve high-throughput while
            maintaining appropriate memory constraints. However,
            batch_size is a useful feature for end-users to be able to
            toggle.

    Returns:
            - {embedding_size: Tensor} where embedding_size can
                be any of [4096, 2048, 512, 128, 20]. The embedding
                Tensor is float32 (or signed int for 20-dim),
                n_sounds x n_frames x dim.
            - Tensor: Frame-center timestamps, 1d.
    """

    # Assert audio is of correct shape
    if audio.ndim != 2:
        raise ValueError(
            "audio input tensor must be 2D with shape (batch_size, num_samples)"
        )

    # Make sure the correct model type was passed in
    if not isinstance(model, RandomProjectionMelEmbedding):
        raise ValueError(
            f"Model must be an instance of {RandomProjectionMelEmbedding.__name__}"
        )

    # Send the model to the same device that the audio tensor is on.
    model = model.to(audio.device)

    # Split the input audio signals into frames and then flatten to create a tensor
    # of audio frames that can be batch processed. We will unflatten back out to
    # (audio_baches, num_frames, embedding_size) after creating embeddings.
    frames, timestamps = frame_audio(
        audio,
        frame_size=model.n_fft,
        frame_rate=frame_rate,
        sample_rate=RandomProjectionMelEmbedding.sample_rate,
    )
    audio_batches, num_frames, frame_size = frames.shape
    frames = frames.flatten(end_dim=1)

    # We're using a DataLoader to help with batching of frames
    dataset = torch.utils.data.TensorDataset(frames)
    loader = torch.utils.data.DataLoader(
        dataset, batch_size=batch_size, shuffle=False, drop_last=False
    )

    # Put the model into eval mode, and don't compute any gradients.
    model.eval()
    with torch.no_grad():
        # Iterate over all batches and accumulate the embeddings
        list_embeddings: DefaultDict[int, List[Tensor]] = defaultdict(list)
        for batch in loader:
            result = model(batch[0])
            for size, embedding in result.items():
                list_embeddings[size].append(embedding)

    # Concatenate mini-batches back together and unflatten the frames back
    # to audio batches
    embeddings: Dict[int, Tensor] = {}
    for size, embedding in list_embeddings.items():
        embeddings[size] = torch.cat(embedding, dim=0)
        embeddings[size] = embeddings[size].unflatten(0, (audio_batches, num_frames))

    return embeddings, timestamps
