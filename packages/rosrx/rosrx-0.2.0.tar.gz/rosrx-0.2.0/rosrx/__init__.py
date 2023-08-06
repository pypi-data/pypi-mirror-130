import pkg_resources

if pkg_resources.get_distribution('rx').version.startswith('1.'):
    # Legacy version of rx
    from .observabletopic_1x import observabletopic
    from .topicobserver_1x import TopicObserver
else:
    from .observabletopic import observabletopic
    from .topicobserver import TopicObserver
