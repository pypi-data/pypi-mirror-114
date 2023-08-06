from rest_framework.serializers import ModelSerializer, SerializerMethodField

from drf_elastic_filter.utils import str_to_class


class ElasticOurFilter:
    def __init__(self, class_model, context):

        self.ctx = context
        self.model = class_model
        self.other = self.get_other_fields()

    def get_other_fields(self):
        other = {}
        try:
            for item in self.ctx['request']:

                other[item] = self.ctx['keys_class'][item]
            else:
                other.pop('scaffold', None)
        except:
            pass
        return other

    def generate_serializer(self):
        """Generate main serializer

        :return : A serializer.
        """
        ctx_fields = self.ctx['request']['scaffold'][0].split(',')
        attr = {}
        for item in self.other:
            # Field
            reg = item.replace('set_', '')
            req = {'scaffold': self.ctx['request'][item]}
            attr[reg] = SerializerMethodField()
            # Method, get_`field`
            x = {'request': req,
                 'keys_class': {item: self.ctx['keys_class'][item]}}

            attr['get_' + reg] = self.serializer_method(self.other[item], x)

            ctx_fields.append(reg)

        class Meta:
            model = self.model
            fields = ctx_fields

        attr['Meta'] = Meta

        return type('ElasticSerializer', (ModelSerializer,), attr)

    def serializer_method(self, module_path, context):
        """Generate Serializer Method dynamically.

        :param module_path: "my_app.models.MyClass"
        :param context
        :return get_`field` method.
        """
        obj = str_to_class(module_path)
        cls = ElasticOurFilter(obj, {'request': context['request'],
                                     'keys_class': context['keys_class']})

        def get_field(self, instance):
            try:
                from django.db.models import Q
                model_class = obj.objects.filter(Q(user_id=instance.user.id)).first()
                cls2 = cls.generate_serializer()
                serializer = cls2(model_class)
                return serializer.data
            except Exception as e:
                raise ValueError(e)

        return get_field
