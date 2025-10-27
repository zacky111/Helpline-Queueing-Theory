def simulate_queues(call_data, num_queues=3, queue_capacity=5):
    """
    Symulacja kolejek z dokładnym oznaczaniem przyjętych/odrzuconych zgłoszeń.
    """
    queues = [[] for _ in range(num_queues)]
    rejected_calls = 0
    timeline = []
    occupancy = []
    accepted_flags = []  # True = przyjęte, False = odrzucone

    for _, call in call_data.iterrows():
        arrival = call['arrival_time']
        service = call['service_time']

        # Czyszczenie kolejek z zakończonych zgłoszeń
        for q in queues:
            while q and q[0] <= arrival:
                q.pop(0)

        free_queues = [q for q in queues if len(q) < queue_capacity]

        if free_queues:
            target_queue = min(free_queues, key=len)
            target_queue.append(arrival + service)
            accepted_flags.append(True)
        else:
            rejected_calls += 1
            accepted_flags.append(False)

        # zapis stanu kolejek
        timeline.append(arrival)
        occupancy.append([len(q) for q in queues])

    stats = {
        'total_calls': len(call_data),
        'rejected_calls': rejected_calls,
        'accepted_calls': len(call_data) - rejected_calls,
        'queues_final_state': [len(q) for q in queues],
        'timeline': timeline,
        'occupancy': occupancy,
        'accepted_flags': accepted_flags
    }

    return stats
