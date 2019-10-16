from rest_framework.renderers import JSONRenderer


class MyJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # render方法为将所有响应的结果(dict)转化为json
        # data为方法中return Response(serializer.data)
        try:
            code = data.pop('code')
        except:
            code = 200
        try:
            msg = data.pop('msg')
        except:
            msg = '请求成功'
        try:
            result = data.pop('data')
        except:
            result = data
        renderer_context['response'].status_code = 200
        res = {
            'code': code,
            'msg': msg,
            'data': result
        }
        return super().render(res)
    #
