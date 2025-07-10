class BookAuthorAI:
    def __init__(self):
        self.book_title = None
        self.target_age_group = None
        self.book_type = None  # 'book' or 'novel'
        self.category = None # e.g., 'history', 'art' for book; 'love', 'sci-fi' for novel

        self.chapter_plan = [] # List of chapter titles or descriptions
        self.approved_chapter_plan = False

        self.written_chapters = {} # Dict mapping chapter_title: content

        self.current_interaction_state = "awaiting_title"
        # Possible states: awaiting_title, awaiting_age, awaiting_type, awaiting_category,
        # awaiting_plan_approval, writing_chapters, awaiting_formatting_choice, done

        self.book_content_for_formatting = ""

    def start_interaction(self):
        self.current_interaction_state = "awaiting_title"
        return "Hello! I am your AI Book Authoring Assistant. I can help you create a book or novel. To start, what is the title of your book?"

    def process_user_response(self, user_response):
        response_message = ""
        if self.current_interaction_state == "awaiting_title":
            self.book_title = user_response
            self.current_interaction_state = "awaiting_age"
            response_message = f"Great! The title of your book is '{self.book_title}'. Now, what is the target age group for this book? (e.g., Children, Young Adult, Adults)"
        elif self.current_interaction_state == "awaiting_age":
            self.target_age_group = user_response
            self.current_interaction_state = "awaiting_type"
            response_message = f"Understood. Target age group: {self.target_age_group}. Is this a 'book' (e.g., non-fiction, educational) or a 'novel' (e.g., fiction story)?"
        elif self.current_interaction_state == "awaiting_type":
            user_response_lower = user_response.lower()
            if user_response_lower in ['book', 'novel']:
                self.book_type = user_response_lower
                self.current_interaction_state = "awaiting_category"
                if self.book_type == 'book':
                    response_message = f"Okay, it's a '{self.book_type}'. What is the category? (e.g., History, Science, Art, Technology, Self-help)"
                else: # novel
                    response_message = f"Okay, it's a '{self.book_type}'. What is the genre? (e.g., Fantasy, Sci-Fi, Mystery, Romance, Thriller)"
            else:
                response_message = "Please respond with either 'book' or 'novel'."
        elif self.current_interaction_state == "awaiting_category":
            self.category = user_response
            self.current_interaction_state = "generating_plan" # Next logical step
            # For now, we'll just confirm. Plan generation comes next.
            response_message = f"Excellent! Category/Genre: '{self.category}'. I have all the initial details. Next, I will generate a chapter plan for your {self.book_type} titled '{self.book_title}' for {self.target_age_group} in the {self.category} category."
            # In a fuller implementation, this is where we'd call _generate_chapter_plan()
            # and then transition to awaiting_plan_approval state.
            # For this step, we stop here for processing initial inputs.
            # We will change state to awaiting_plan_approval after plan generation in a future step.
            self.current_interaction_state = "awaiting_plan_generation" # Placeholder for next step
            # The actual plan generation and requesting approval will be separate.
            # For now, this indicates data collection is done.
            # TODO: Transition to a state where plan generation is triggered.
            # For now, let's assume we will call _generate_chapter_plan and then ask for approval.
            # This message is a stub for that.
            response_message = (f"Got it! Category/Genre: '{self.category}'.\n"
                              f"Book Title: '{self.book_title}'\n"
                              f"Target Age: '{self.target_age_group}'\n"
                              f"Type: '{self.book_type}'\n"
                              f"I will now work on a chapter plan for you. Please give me a moment.")
            # Here, we would internally call something like self._generate_chapter_plan()
            # and then the next response would be the plan itself, asking for approval.
            # For this step, we'll just confirm receipt of info.
            self.current_interaction_state = "ready_for_plan_generation"

        else:
            response_message = "I'm not sure how to process that at this stage."

        return response_message

    def _generate_chapter_plan(self):
        # Placeholder - will be implemented later
        pass

    def _write_chapter_content(self, chapter_title):
        # Placeholder - will be implemented later
        pass

    def _format_book(self, format_type):
        # Placeholder - will be implemented later
        pass

if __name__ == '__main__':
    ai_author = BookAuthorAI()
    print(f"AI: {ai_author.start_interaction()}")

    # Simulate user responses
    user_inputs = [
        "The Cosmic Labyrinth", # Title
        "Young Adult",          # Age Group
        "Novel",                # Type
        "Sci-Fi"                # Category
    ]

    for user_input in user_inputs:
        print(f"User: {user_input}")
        ai_response = ai_author.process_user_response(user_input)
        print(f"AI: {ai_response}")
        if ai_author.current_interaction_state == "ready_for_plan_generation":
            print("\nAI: All initial information gathered. Ready to generate chapter plan.")
            break

    # Expected final state for this phase
    print(f"\n--- Final AI State ---")
    print(f"Title: {ai_author.book_title}")
    print(f"Age Group: {ai_author.target_age_group}")
    print(f"Book Type: {ai_author.book_type}")
    print(f"Category: {ai_author.category}")
    print(f"Interaction State: {ai_author.current_interaction_state}")
