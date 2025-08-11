import types

from snake_case.audio import sound


def test_sound_manager_initializes(monkeypatch):
    class DummySound:
        def __init__(self, *args, **kwargs):
            pass
        def set_volume(self, vol):
            pass
        def play(self, loops=0):
            pass

    class DummyMixer:
        def init(self):
            pass
        Sound = DummySound

    dummy_pygame = types.SimpleNamespace(mixer=DummyMixer(), error=Exception)
    monkeypatch.setattr(sound, "pygame", dummy_pygame)

    mgr = sound.SoundManager()
    assert mgr.loaded
    mgr.play_music()
    mgr.play_munch()
    mgr.play_death()


def test_sound_manager_handles_init_failure(monkeypatch):
    class DummySound:
        def __init__(self, *args, **kwargs):
            pass
        def set_volume(self, vol):
            pass
        def play(self, loops=0):
            pass

    class DummyMixer:
        def init(self):
            raise sound.pygame.error("boom")
        Sound = DummySound

    dummy_pygame = types.SimpleNamespace(mixer=DummyMixer(), error=RuntimeError)
    monkeypatch.setattr(sound, "pygame", dummy_pygame)

    mgr = sound.SoundManager()
    assert not mgr.loaded
    mgr.play_music()
    mgr.play_munch()
    mgr.play_death()
