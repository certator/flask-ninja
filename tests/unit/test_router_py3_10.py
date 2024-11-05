# type: ignore
# ^ type check with python 3.9 fails because of "A | B" union syntax
from pydantic import BaseModel

from flask_ninja import Query
from flask_ninja.operation import Callback
from flask_ninja.router import Router
from flask_ninja.utils import create_model_field


def test_add_route_union():
    router = Router()
    callback = Callback(
        name="some_name",
        url="some_url",
        method="some_callback_method",
        response_codes={},
    )

    param = create_model_field(name="some_param", type_=int, field_info=Query())

    class Response200(BaseModel):
        status: str

    class Response400(BaseModel):
        error: str

    @router.add_route(
        "GET",
        "/foo",
        responses={200: Response200, 400: Response400},
        auth="some_auth",
        summary="some_summary",
        description="some_description",
        params=[param],
        callbacks=[callback],
    )
    def sample_method() -> Response200 | Response400:
        return Response200(status="foo")

    assert len(router.operations) == 1
    assert router.operations[0].path == "/foo"
    assert router.operations[0].method == "GET"
    assert str(router.operations[0].responses) == str(
        {
            200: create_model_field(name="Response 200", type_=Response200),
            400: create_model_field(name="Response 400", type_=Response400),
        }
    )
    assert router.operations[0].callbacks == [callback]
    assert router.operations[0].summary == "some_summary"
    assert router.operations[0].description == "some_description"
    assert router.operations[0].params == [param]
