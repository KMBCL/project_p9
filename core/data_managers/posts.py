from dataclasses import dataclass


from django.db.models import Q, Exists, OuterRef

from core.models.user import User
from core.models.ticket import Ticket
from core.models.review import Review
from core.data_managers.helper.merge_posts import MergePostsConfig, merge_posts


@dataclass
class PostConfig:
    request_user: User


class PostService:

    def get_user_tickets(self, config: PostConfig):
        user_reviews = Review.objects.filter(
            user=config.request_user,
            ticket=OuterRef("pk"),
        )
        tickets = Ticket.objects.filter(Q(user=config.request_user)).select_related()
        tickets = tickets.annotate(has_user_reviews=Exists(user_reviews))
        return tickets

    def get_user_reviews(self, config: PostConfig):
        reviews = (
            Review.objects.filter(
                Q(user=config.request_user) | Q(ticket__user=config.request_user),
            )
            .distinct()
            .select_related()
        )
        return reviews

    def get_posts(self, config: PostConfig) -> list[Review | Ticket]:
        merge_posts_config = MergePostsConfig(
            tickets=self.get_user_tickets(config),
            reviews=self.get_user_reviews(config),
        )

        return merge_posts(merge_posts_config)
