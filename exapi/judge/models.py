from dataclasses import dataclass


@dataclass
class Submission:
    time: str
    memory: int
    stdout: str
    stderr: str
    compile_output: str

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            time=dikt["time"],
            memory=dikt["memory"],
            stdout=dikt["stdout"],
            stderr=dikt["stderr"],
            compile_output=dikt["compile_output"],
        )
