"""Global fixtures for integration_blueprint integration."""
# Fixtures allow you to replace functions with a Mock object. You can perform
# many options via the Mock to reflect a particular behavior from the original
# function that you want to see without going through the function's actual logic.
# Fixtures can either be passed into tests as parameters, or if autouse=True, they
# will automatically be used across all tests.
#
# Fixtures that are defined in conftest.py are available across all tests. You can also
# define fixtures within a particular test file to scope them locally.
#
# pytest_homeassistant_custom_component provides some fixtures that are provided by
# Home Assistant core. You can find those fixture definitions here:
# https://github.com/MatthewFlamm/pytest-homeassistant-custom-component/blob/master/pytest_homeassistant_custom_component/common.py
#
# See here for more info: https://docs.pytest.org/en/latest/fixture.html (note that
# pytest includes fixtures OOB which you can use as defined on this page)
from unittest.mock import Mock, patch

from homeassistant.core import callback
import pytest

pytest_plugins = "pytest_homeassistant_custom_component"

# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


# This fixture is used to prevent HomeAssistant from attempting to create and dismiss persistent
# notifications. These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


class MQTTMock:
    mqtt_is_connected: Mock
    mqtt_publish: Mock
    async_subscribe: Mock


@pytest.fixture()
def mqtt_patch():

    @callback
    def _unsub_mqtt_subscribe():
        pass

    with patch(
        "homeassistant.components.mqtt.is_connected"
    ) as mqtt_is_connected, patch(
        "homeassistant.components.mqtt.publish"
    ) as mqtt_publish, patch(
        "homeassistant.components.mqtt.async_subscribe",
        return_value = _unsub_mqtt_subscribe
    ) as async_subscribe:
        mock = MQTTMock()
        mock.mqtt_is_connected = mqtt_is_connected
        mock.mqtt_publish = mqtt_publish
        mock.async_subscribe = async_subscribe
        yield mock


@pytest.fixture()
def mqtt_available(mqtt_patch: MQTTMock):
    mqtt_patch.mqtt_is_connected.return_value = True
    return mqtt_patch
