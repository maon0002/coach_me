# import logging
# from django.http import JsonResponse, HttpResponse
# from django.template import TemplateDoesNotExist, loader
# from django.utils.deprecation import MiddlewareMixin
#
#
# class CatchAllExceptionsMiddleware(MiddlewareMixin):
#     def process_exception(self, request, exception):
#         # Log the exception
#         logging.exception("Unhandled exception occurred: ")
#
#         # Check if the exception is a TemplateDoesNotExist exception
#         if isinstance(exception, TemplateDoesNotExist):
#             # Customize the response for template not found error
#             response = self.handle_template_not_found(request)
#         else:
#             # Customize the response for other exceptions
#             response = self.handle_other_exceptions(request, exception)
#
#         return response
#
#     def handle_template_not_found(self, request):
#         # Customize the response for template not found error
#         context = {}
#         template = loader.get_template('core/template_not_found.html')
#         return HttpResponse(template.render(context, request), status=404)
#
#     def handle_other_exceptions(self, request, exception):
#         # Customize the response for other exceptions
#         error_message = "An internal server error occurred. Please try again later."
#         response_data = {
#             'error': error_message,
#         }
#         return JsonResponse(response_data, status=500)


from django.template.exceptions import TemplateDoesNotExist
from django.http import HttpResponseServerError
from django.shortcuts import render


class CatchAllExceptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except TemplateDoesNotExist:
            # Handle TemplateDoesNotExist exception by rendering the custom template_not_found.html
            return render(request, 'core/template_not_found.html', status=404)
        except Exception as e:
            # Handle other exceptions by returning a generic error response
            response = HttpResponseServerError('Internal Server Error', status=500)

        return response
