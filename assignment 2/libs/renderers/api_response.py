from rest_framework.renderers import JSONRenderer


class CustomJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response", None)

        # Get status code from the response
        status_code = response.status_code if response else 200

        # If 'message' is not included in the response, set a default message
        message = "Success" if str(status_code).startswith("2") else "Error"

        response_data = {
            'code': status_code,
            'message': message,
            'data': data
        }
        return super().render(response_data, accepted_media_type, renderer_context)
