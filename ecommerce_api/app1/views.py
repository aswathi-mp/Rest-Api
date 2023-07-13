from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Customer,Product
from .serializers import CustomerSerializer,ProductSerializer
from datetime import date



class CustomerView(APIView):

	def get(self,request,id=None):
		if id == None:
			customer = Customer.objects.all()
			serializer = CustomerSerializer(customer, many=True)
			return Response({'data':serializer.data})
		else:
			try:
				customer = Customer.objects.get(id=id)
				serializer = CustomerSerializer(customer)
				return Response({'data':serializer.data})
			except Customer.DoesNotExist:
				return Response({'data': None,'errors':'Invalid Customer ID'})

	def post(self,request):
		serializer = CustomerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'data':serializer.data})
		else:
			return Response({'data':None,'errors':serializer.errors})

	def put(self,request,id):
		try:
			customer = Customer.objects.get(id=id)
			serializer = CustomerSerializer(customer,data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'data':serializer.data,'success':True})
			else:
				return Response({'data':None,'success':False,'errors':serializer.errors})
		except Customer.DoesNotExist:
			return Response({'error':"Invalid customer id",'success':False})
	
	def delete(self,request,id):
		try:
			customer = Customer.objects.get(id=id)
			customer.delete()
			return Response({'success':True})
		except Customer.DoesNotExist:
			return Response({'error':"Invalid customer id",'success':False})


class ProductView(APIView):

	def get(self,request,id=None):
		if id == None:
			products = Product.objects.all()
			serializer = ProductSerializer(products, many=True)
			return Response({'data':serializer.data})
		else:
			try:
				product = Product.objects.get(id=id)
				serializer = ProductSerializer(product)
				return Response({'data':serializer.data})
			except Product.DoesNotExist:
				return Response({'data': None,'error':'Invalid Product ID'})

	def post(self,request):
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'data':serializer.data,'success':True})
		else:
			return Response({'data':None,'success':False,'error':serializer.errors})

	def put(self,request,id):
		try:
			product = Product.objects.get(id=id)
			serializer = ProductSerializer(product,data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'data':serializer.data,'success':True})
			else:
				return Response({'data':None,'success':False,'error':serializer.errors})
		except Product.DoesNotExist:
				return Response({'error':"Invalid product id",'success':False})

	def delete(self,request,id):	
		try:
			product = Product.objects.get(id=id)
			product.delete()
			return Response({'success':True})
		except Product.DoesNotExist:
			return Response({'error':"Invalid product id",'success':False})

class ActiveProduct(APIView):
    
    def put(self,request,id):
        try:
            product = Product.objects.get(id=id)
            product.is_active = True
            product.save()
            message = "The Product has been activated successfully"
            return Response({'message':message,'success':True})
        except Product.DoesNotExist :
            return Response({'error':"Invalid product id",'success':False})
        
class InactiveProduct(APIView):
    
    def put(self,request,id):
        try:
            product = Product.objects.get(id=id)
            current_dt = date.today()
            created_dt = product.created_date
            days = (current_dt - created_dt).days
            if (int(days) < 60):
                message = "The product can only be deactivated if it has been registered before two months"
                return Response({'message': message,'success':False})
            else:
                product.is_active = False
                product.save()
                serializer = ProductSerializer(product)
                message = "The product has been deactivated successfully"
                return Response({'message':message,'success':True})
        except Product.DoesNotExist:
            return Response({'error':"Invalid product id",'success':False})