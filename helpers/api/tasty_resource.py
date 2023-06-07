from tastypie.exceptions import BadRequest


def create_resource(resource_model, request, obj_dict):
    res = resource_model()

    data = res.alter_deserialized_detail_data(request, obj_dict)
    bundle = res.build_bundle(data=data, request=request)
    if res.is_valid(bundle):
        try:
            obj = res.obj_create(bundle, request=request)
            if obj is not None:
                return True, obj
            else:
                return False, None

        except BadRequest as e:
            return False, e
    else:
        return False, bundle.errors
