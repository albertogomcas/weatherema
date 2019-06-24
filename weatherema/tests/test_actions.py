from weatherema.actions import Action


def test_action_run(mocker):
    a = Action("TEST_ACTION", func=lambda x: x)
    mocker.patch.object(a, 'func')
    a.run()
    a.func.assert_called_once()
