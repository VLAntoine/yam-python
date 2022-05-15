from abc import ABC


class Subscriber(ABC):
    """
    The abstract subscriber class from the observer pattern.
    A subscriber receives notification from a publisher and updates its attributes.
    """
    def __init__(self):
        """
        The constructor of the Subscriber class.
        """
        pass

    def update_subscriber(self, context):
        """
        Updates the subscriber attribute, according to the context sent by the publisher.
        """
        pass


class Publisher(ABC):
    """
    The abstract publisher class from the observer pattern.
    A publisher can add or delete subscribers to its list of subscribers and send them notification.
    """
    def __init__(self):
        """
        The constructor of the Publisher class.
        subscribers is a list of the Subscribers of the publisher.
        """
        self.__subscribers = []

    @property
    def subscribers(self):
        """
        The getter of the subscribers list.
        """
        return self.__subscribers

    def subscribe(self, subscriber: Subscriber):
        """
        Append a subscriber to the subscribers list of the publisher.
        """
        self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Subscriber):
        """
        Remove a subscriber from the subscribers list of the publisher.
        """
        self.__subscribers.remove(subscriber)

    def notify_subscriber(self, context):
        """
        Notify the subscribers by sending them the context.
        """
        for subscriber in self.__subscribers:
            subscriber.update_subscriber(context)





