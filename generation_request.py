class GenerationRequest:
    def __init__(self) -> None:
        self.max_new_length = None
        self.max_context_length = None
        self.repetition_penalty = None
        self.repetition_penalty_slope = None
        self.repetition_penalty_range = None
        self.prompt = None
        self.temperature = None
        self.top_p = None
        self.top_k = None
        self.top_a = None
        self.tail_free_sampling = None
        self.typical = None
        self.batch_count = None
