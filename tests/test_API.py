from Data import API


class FakeResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


def test_get_wave_data_returns_parsed_json(monkeypatch, fake_api_response):
    captured = {}

    def fake_get(url, params=None):
        captured["url"] = url
        captured["params"] = params
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(API.requests, "get", fake_get)

    result = API.get_wave_data(33.66, -117.99)

    assert result == fake_api_response


def test_get_wave_data_calls_correct_url_and_params(monkeypatch, fake_api_response):
    captured = {}

    def fake_get(url, params=None):
        captured["url"] = url
        captured["params"] = params
        return FakeResponse(fake_api_response)

    monkeypatch.setattr(API.requests, "get", fake_get)

    API.get_wave_data(33.66, -117.99)

    assert captured["url"] == "https://marine-api.open-meteo.com/v1/marine"
    assert captured["params"]["latitude"] == 33.66
    assert captured["params"]["longitude"] == -117.99
    assert "wave_height" in captured["params"]["hourly"]
    assert "swell_wave_direction" in captured["params"]["hourly"]
