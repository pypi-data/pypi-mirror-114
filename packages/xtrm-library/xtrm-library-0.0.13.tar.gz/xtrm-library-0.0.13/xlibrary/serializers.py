from rest_framework import serializers
#from datetime import date
class ExtraFieldsSerializer(serializers.ModelSerializer):
    # vdate=serializers.SerializerMethodField('getDate')
    # def getDate(self,*args,**kwargs):
    #     return date.today()
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ExtraFieldsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
    class Meta:
        # extra_fields=['vdate']
        # read_only_fields=('vdate')
        abstract=True

class NumericField(serializers.DecimalField):
    """
    We wanted to be able to receive an empty string ('') for a decimal field
    and in that case turn it into a None number
    """
    def to_internal_value(self, data):
        if data == '':
            return None

        return super(NumericField, self).to_internal_value(data)


