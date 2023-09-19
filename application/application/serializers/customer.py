from rest_framework import serializers

from application.models import Address, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["address"]

    def to_representation(self, instance):
        ret = super(CustomerSerializer, self).to_representation(instance)
        address = instance.address
        ret["address"] = (
            address.prefecture
            + address.municipalities
            + address.house_no
            + address.other
        )
        return ret


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
