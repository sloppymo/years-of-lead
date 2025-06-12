import pathlib
import pytest

# Skip this test completely if running in a headless environment without Tk support
pytest.importorskip("tkinter")

from gui.main_gui import YearsOfLeadGUI


def test_gui_save_and_advance(tmp_path, monkeypatch):
    """Smoke-test GUI logic: advance a turn and save game without rendering the window."""
    # Change working directory to a fresh tmp dir so GUI writes there
    monkeypatch.chdir(tmp_path)

    # Instantiate the GUI, but do not call mainloop so no window is shown
    app = YearsOfLeadGUI()

    # Record initial turn
    initial_turn = app.game_state.turn_number

    # Advance one turn using the GUI method
    app.advance_turn()
    assert app.game_state.turn_number == initial_turn + 1

    # Call save_game – this should create the pickle file without raising
    app.save_game()

    # Verify the save file exists
    save_file = pathlib.Path("savegames/current_game.pkl")
    assert save_file.exists(), "GUI save_game did not create save file"
