class ResumeNotFoundException(Exception):
    def __init__(self, resume_id: int):
        self.message = f"Resume with id {resume_id} not found"
        super().__init__(self.message)


class JobNotFoundException(Exception):
    def __init__(self, jd_id: int):
        self.message = f"Job description with id {jd_id} not found"
        super().__init__(self.message)


class AnalysisNotFoundException(Exception):
    def __init__(self, analysis_id: int):
        self.message = f"Analysis with id {analysis_id} not found"
        super().__init__(self.message)


class GeminiCallFailedException(Exception):
    def __init__(self, step: str, reason: str):
        self.message = f"Gemini call failed at step '{step}': {reason}"
        super().__init__(self.message)


class EmbeddingFailedException(Exception):
    def __init__(self, skill: str, reason: str):
        self.message = f"Embedding failed for skill '{skill}': {reason}"
        super().__init__(self.message)


class PDFParsingFailedException(Exception):
    def __init__(self, reason: str):
        self.message = f"PDF parsing failed: {reason}"
        super().__init__(self.message)
