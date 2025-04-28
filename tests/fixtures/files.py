import pytest


@pytest.fixture
def document_files():
    document1 = open("./fixtures/files/document1.pdf", "rb")
    document2 = open("./fixtures/files/document2.png", "rb")

    yield [document1, document2]

    document1.close()
    document2.close()


@pytest.fixture
def media_files():
    image1 = open("./fixtures/files/image1.png", "rb")
    image2 = open("./fixtures/files/image2.jpg", "rb")
    video1 = open("./fixtures/files/video1.mp4", "rb")

    yield [image1, image2, video1]

    image1.close()
    image2.close()
    video1.close()


@pytest.fixture
def media_data(media_files):
    data = {}
    for i, file in enumerate(media_files):
        key = f"media_files[{i}]"
        data[key] = file

    yield data


@pytest.fixture
def invalid_media_data(document_files):
    data = {}
    for i, file in enumerate(document_files):
        key = f"media_files[{i}]"
        data[key] = file

    yield data


@pytest.fixture
def route_data(media_files):
    data = {}
    for i, file in enumerate(media_files):
        key = f"route_files[{i}]"
        data[key] = file

    yield data
