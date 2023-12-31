def nice_choice(request):
    return "Nice choice!" + "\U0001F603"


def interesting_opinion(request):
    return "Interesting opinion" + "\U0001F923"


def preach_bro(request):
    return "Preach bro, preach"


comment_dict = {
    1: nice_choice,
    2: interesting_opinion,
    4: preach_bro,
    5: interesting_opinion,
}


class Commentator:
    def __init__(self, choices_listener=None):
        self.comment_dict = comment_dict
        self.choices_listener = None
        if choices_listener is not None:
            self.choices_listener = dict.fromkeys(choices_listener, 0)

    """
	Update info for selected choice
	@param choice_id - id of selected choice
	"""

    def update_listener(self, choice_id):
        if self.choices_listener is not None and choice_id in self.choices_listener:
            self.choices_listener[choice_id] += 1

    """
	Handle choice to update info and give out comment if possible
	@param request - current request
	@param choice_id - id of selected choice
	"""

    def handle(self, request, choice_id):
        handler = self.comment_dict.get(choice_id, None)

        self.update_listener(choice_id)

        if handler is not None:
            return handler(request)
        return None
