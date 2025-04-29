def user_data_processor(request):
    if request.user.is_authenticated:
        user_type = request.session.get('user_type')
        user_name = request.session.get('user_name')
        profile_picture = request.session.get('profile_picture')
        return  {'user_type': user_type, 'user_name': user_name, 'profile_picture': profile_picture}
    return {}