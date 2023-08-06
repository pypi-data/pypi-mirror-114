from rest_framework import serializers

from portfolio.models import Security, Account


class SecuritySerializer(serializers.ModelSerializer):
    """
    Serializing all the Securities
    """
    tracker_name = serializers.CharField(source='price_tracker.name')

    class Meta:
        model = Security
        fields = ('ticker', 'name', 'id', 'tracker_name')


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializing all the Securities
    """
    class Meta:
        model = Account
        fields = ('base_currency', 'name', 'id')
