import pytest
from unittest.mock import MagicMock, AsyncMock
from unittest import IsolatedAsyncioTestCase
from pydantic import BaseModel, HttpUrl
from src.rest_api_client.lib import (
    RestAPI,
    Endpoint,
    HTTPMethod,
    MissingMethodName,
    BearerHeaderToken,
)
import httpx

CHUCK_BASE_URL = "https://api.chucknorris.io/jokes"

example_response = {
    "categories": [],
    "created_at": "2020-01-05 13:42:24.40636",
    "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
    "id": "fMxB6_A2Qku_tKeo5jzRiA",
    "updated_at": "2020-01-05 13:42:24.40636",
    "url": "https://api.chucknorris.io/jokes/fMxB6_A2Qku_tKeo5jzRiA",
    "value": "America's next top model is really a competition of who gets to have Chuck Norris's child.",  # noqa: E501
}

categories = [
    "animal",
    "career",
    "celebrity",
    "dev",
    "explicit",
    "fashion",
    "food",
    "history",
    "money",
    "movie",
    "music",
    "political",
    "religion",
    "science",
    "sport",
    "travel",
]

animal_category = {
    "categories": ["animal"],
    "created_at": "2020-01-05 13:42:19.576875",
    "icon_url": "https://assets.chucknorris.host/img/avatar/chuck-norris.png",
    "id": "bmom6jqftpqgokh8adtolw",
    "updated_at": "2020-01-05 13:42:19.576875",
    "url": "https://api.chucknorris.io/jokes/bmom6jqftpqgokh8adtolw",
    "value": "Chuck Norris once rode a nine foot grizzly bear through an automatic car wash, instead of taking a shower.",
}


class JokeModel(BaseModel):
    id: str
    created_at: str
    updated_at: str
    icon_url: str
    categories: list
    url: HttpUrl
    value: str


def test_get_rest_api():
    endpoints = [
        Endpoint(
            name="get_joke",
            path="/random",
            method=HTTPMethod.GET,
            model=JokeModel,
            query_parameters=[("category", str)],
        ),
        Endpoint(
            name="get_categories",
            path="/categories",
            method=HTTPMethod.GET,
        ),
        Endpoint(name="get_search", path="/search", query_parameters=[("query", str)]),
    ]
    client = MagicMock(spec=httpx.Client)
    client.get().json.side_effect = [
        example_response,
        example_response,
        example_response,
        categories,
        example_response,
    ]
    api = RestAPI(api_url=CHUCK_BASE_URL, driver=client)
    api.register_endpoints(endpoints)

    joke = api.call_endpoint("get_joke")
    assert isinstance(joke, JokeModel)
    for key, item in example_response.items():
        assert item == getattr(joke, key)

    joke2 = api.get_joke()
    assert joke == joke2

    api.get_joke(category="doesitwork?")

    assert api.get_categories() == categories

    api.get_search(query="something")


def make_pantry_api():
    client = MagicMock()
    api = RestAPI(
        api_url="https://getpantry.cloud/apiv1",
        driver=client,
        endpoints=[
            Endpoint(name="get_pantry", path="/pantry/{pantry_id}"),
            Endpoint(
                name="get_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
                method=HTTPMethod.GET,
            ),
            Endpoint(
                name="create_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
                method=HTTPMethod.POST,
            ),
            Endpoint(
                name="update_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
                method=HTTPMethod.PUT,
            ),
            Endpoint(
                name="delete_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
                method=HTTPMethod.DELETE,
            ),
        ],
    )
    return api


def test_pantry_api():
    api = make_pantry_api()
    api.get_pantry(pantry_id="123")
    api.create_basket(pantry_id="123", basket_id="234", data={"key": "value"})
    api.update_basket(pantry_id="123", basket_id="234", data={"key2": "value2"})
    api.get_basket(pantry_id="123", basket_id="234")
    api.delete_basket(pantry_id="123", basket_id="234")


@pytest.mark.asyncio
async def test_async():
    api = make_pantry_api()
    api.driver = MagicMock()
    json_mock = MagicMock()

    api.driver.get = AsyncMock()
    json_mock.json.return_value = "GET"
    api.driver.get.side_effect = json_mock

    api.driver.post = AsyncMock()
    json_mock.json.return_value = "POST"
    api.driver.post.side_effect = json_mock

    api.driver.put = AsyncMock()
    json_mock.json.return_value = "PUT"
    api.driver.put.side_effect = json_mock

    api.driver.delete = AsyncMock()
    json_mock.json.return_value = "DELETE"
    api.driver.delete.side_effect = json_mock

    await api.async_get_pantry(pantry_id="123") == "GET"

    await api.async_create_basket(
        pantry_id="123", basket_id="234", data={"key": "value"}
    ) == "CREATE"
    await api.async_update_basket(
        pantry_id="123", basket_id="234", data={"key2": "value2"}
    ) == "UPDATE"

    await api.async_get_basket(pantry_id="123", basket_id="234") == "GET"

    await api.async_delete_basket(pantry_id="123", basket_id="234") == "DELETE"


def test_pantry_api_with_aliases():
    client = MagicMock()
    api = RestAPI(
        api_url="https://getpantry.cloud/apiv1",
        driver=client,
        endpoints=[
            Endpoint(name="get_pantry", path="/pantry/{pantry_id}"),
            Endpoint(
                name="get_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
            ),
            Endpoint(
                name="create_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
            ),
            Endpoint(
                name="update_basket",
                path="/pantry/{pantry_id}/basket/{basket_id}",
            ),
            Endpoint(
                name="delete_basket", path="/pantry/{pantry_id}/basket/{basket_id}"
            ),
        ],
    )
    api.get_pantry(pantry_id="123")
    api.create_basket(pantry_id="123", basket_id="234", data={"key": "value"})
    api.update_basket(pantry_id="123", basket_id="234", data={"key2": "value2"})
    api.get_basket(pantry_id="123", basket_id="234")
    api.delete_basket(pantry_id="123", basket_id="234")


def test_get_path_parameter():
    api = RestAPI("https://getpantry.cloud/apiv1", MagicMock())
    params: Dict[str, type] = api.get_path_parameters(
        "/pantry/{pantry_id}/basket/{basket_id}"
    )

    assert params[0] == "pantry_id"
    assert params[1] == "basket_id"


def test_notion_bearer():
    auth = BearerHeaderToken(bearer_token="ABC")
    client = MagicMock(auth=auth)
    api = RestAPI(
        api_url="https://api.notion.com/v1",
        driver=client,
        endpoints=[
            Endpoint(name="search", path="/search", method=HTTPMethod.POST),
        ],
        custom_headers={"Notion-Version": "2021-05-13"},
    )
    assert api.search(data={"query": "test"})


def test_missing_method_name():
    with pytest.raises(MissingMethodName):
        api = RestAPI(
            "https://getpantry.cloud/apiv1",
            MagicMock(),
            endpoints=[Endpoint(name="wrong_pantry", path="/pantry/{pantry_id}")],
        )
