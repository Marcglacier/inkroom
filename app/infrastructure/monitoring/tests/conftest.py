from dotenv import load_dotenv

load_dotenv()

import pytest

from app import create_app


@pytest.fixture
def app():

    application = create_app()

    application.config["TESTING"] = True

    return application  