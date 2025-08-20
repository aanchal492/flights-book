# airport/context_processor.py
def last_flight_id(request):
    return {
        'last_flight_id': request.session.get('last_flight_id')
    }
