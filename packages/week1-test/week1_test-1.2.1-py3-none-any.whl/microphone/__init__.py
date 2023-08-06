""" This package contains utilities for configuring, saving, and testing a microphone.

Running the script `configure_input.py` will prompt a user to choose their microphone.
This will save a file to songfp/mic_config/config.ini

`configure_input.load_ini()` will return the name of the saved device from the config.ini file

Provides basic functionality for recording audio from a saved device, and
playing the audio back."""

from typing import Optional, Dict, Tuple, List


__all__ = ["record_audio",
           "play_audio"]


def configure_input():
    from microphone.configure_input import load_ini, get_input_devices, present_menu, save_ini
    savedDevice = load_ini()
    inputDevices = get_input_devices()
    selectedDevice = present_menu(inputDevices, savedDevice)
    print("'{}' selected as input device".format(selectedDevice['name']))
    save_ini(selectedDevice)

def test_input():
    from microphone.context_managers import open_input_device, open_output_device
    from microphone.configure_input import load_ini

    """ Running this function will test the configured microphone - it will record
        audio using the device for RECORD_SECONDS amount of time, and then play back
        the audio. """

    RECORD_SECONDS = 5

    print('Recording audio for {} seconds... (if this hangs, choose a different input device)'.format(RECORD_SECONDS))
    frames, _RATE = record_audio(RECORD_SECONDS)
    print('Finished recording')

    # Playback the recorded digital signal
    print('Playing back recording...')
    play_audio(frames, RECORD_SECONDS)
    print('Finished playback')

def record_audio(time: float, device: Optional[Dict[str, str]] = None) -> Tuple[List[bytes], int]:
    """ Record input stream to in-memory list.

    Parameters
    ----------
    time : float
        The amount of time, in seconds, to record for.

    device : Optional[Dict[str, str]]
        {name : device name,
        index: device index from config prompt}

    Returns
    -------
    Tuple[List[bytes], int]
        The bytes from the recorded signal, and the sample rate."""
    from microphone.config import settings
    from microphone.context_managers import open_input_device

    with open_input_device(device) as mic:
        frames = [mic.read(settings.chunk) for _ in range(0, int(settings.rate / settings.chunk * time))]
    return frames, settings.rate


def play_audio(frames: List[bytes], time: float):
    """ Play an audio stream.

    Parameters
    ----------
    frames : List[bytes]
        The bytes to write to the output stream.

    time : float
        The amount of time to play back (in seconds)"""
    from microphone.config import settings
    from microphone.context_managers import open_output_device

    with open_output_device() as stream:
        for i in range(0, int(settings.rate / settings.chunk * time)):
            stream.write(frames[i], settings.chunk)
