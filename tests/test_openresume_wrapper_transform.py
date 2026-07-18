import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.openresume_wrapper import OpenResumeWrapper


class DummyConfig:
    pass


class Obj:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_work_experience_location_reaches_primary_generator():
    resume = Obj(
        personalInfo=Obj(
            name="Location Test",
            email="location@example.com",
            phone="",
            url="",
            github="",
            linkedin="",
            summary="",
            location="",
        ),
        workExperiences=[
            Obj(
                company="Twin Health",
                jobTitle="Senior AI Engineer",
                date="January 2026 - Present",
                location="Remote",
                descriptions=["Built production systems."],
            )
        ],
        educations=[],
        projects=[],
        skills=[],
        publications=[],
        certifications=[],
        custom=Obj(descriptions=[]),
        settings=Obj(
            fontFamily="OpenSans",
            fontSize="11",
            documentSize="Letter",
            themeColor="#1f2937",
        ),
    )

    transformed = OpenResumeWrapper(DummyConfig()).transform_to_openresume_format(resume)

    assert transformed["workExperiences"][0]["location"] == "Remote"


if __name__ == "__main__":
    test_work_experience_location_reaches_primary_generator()
    print("openresume wrapper transform tests passed")
