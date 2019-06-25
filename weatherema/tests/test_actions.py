from weatherema.actions import Action, UP, DOWN


def test_action_run(mocker):
    a = Action("TEST_ACTION", func=lambda x: x)
    mocker.patch.object(a, 'func')
    a.run()
    a.func.assert_called_once()


def test_up(mocker):
    mocker.patch.object(UP, 'func')
    UP.run()
    UP.func.assert_called_once()


def test_down(mocker):
    mocker.patch.object(DOWN, 'func')
    DOWN.run()
    DOWN.func.assert_called_once()
