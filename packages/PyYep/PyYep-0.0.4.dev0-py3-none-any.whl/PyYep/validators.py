import re
import decimal
import functools
from typing import Any, Callable, TYPE_CHECKING
from collections.abc import Iterable
from .exceptions import ValidationError

if TYPE_CHECKING:
	from .__init__ import InputItem, Schema


def validator(func):
	'''Wraps a Validator method to be used as a validator function

	Parameters
	----------
	func : Callable
	    the function that will be used as validator

	Returns
	-------
	wrapper (Callable)
	    the wrapper function of the decorator
	'''

	@functools.wraps(func)
	def wrapper(*args):
		'''A wrapper function that appends a validator in the input's validators list

		Parameters
		----------
		*args
		    the positional orguments received by the wrapped method

		Returns
		-------
		args[0] (Type[Validator]): the self argument passed to the method being wrapped
		'''

		args[0].input_ = args[0].input_.validate(lambda v: func(*args, v))
		return args[0]

	return wrapper


class Validator():
	'''
	A class to represent a base validator.

	...

	Attributes
	----------
	input_ : any
		the input that will be validated
	name : str
		the name of the input that will be validated

	Methods
	-------
	_set_parent_form(form):
		Set the parent schema

	condition(condition):
		Set a condition for the execution of the previous validator

	modifier(modifier):
		Set a modifier to allow changes in the value after validation

	required(value):
		Verify if the received value is empty

	in_(data_structure, value):
		verifies the presence of a value into a data structure
	'''

	def __init__(self, input_: 'InputItem') -> None:
		'''
		Constructs all the necessary attributes for the base validator object.

		Parameters
		----------
			input_ (InputItem): the input that will be validated
		'''

		self.input_ = input_
		self.name = input_.name

	def condition(self, condition: Callable[[Any], bool]) -> 'Validator':
		'''
		Set a condition for the execution of the previous validator

		Parameters
		----------
		condition : Callable
			a callable that return a boolean that defines if the condition was satisfied

		Returns
		-------
		Validator
		'''

		self.input_.condition(condition)
		return self

	def modifier(self, modifier: Callable[[Any], bool]) -> 'Validator':
		'''
		Set a modifier to allow changes in the value after validation

		Parameters
		----------
		modifier : Callable
			a callable that executes changes in the value after validation

		Returns
		-------
		Validator
		'''

		self.input_.modifier(modifier)
		return self

	def _set_parent_form(self, form: 'Schema') -> None:
		'''
		Set the parent schema of the validator's input

		Parameters
		----------
		form : Schema
			the validator's input parent schema

		Returns
		-------
		None
		'''

		self.input_.form = form

	@validator
	def required(self, value: Any) -> None:
		'''
		Verify if the received value is empty

		Parameters
		----------
		value : (Any)
			the value that will be checked

		Raises
		----------
		ValidationError:
			if the value is empty or None

		Returns
		________
		None
		'''

		if value is None or (not value and value != 0):
			raise ValidationError(self.name, 'Empty value passed to a required input')

	@validator
	def in_(self, data_structure: Iterable, value: Any):
		'''
		Verify if the received value is present in the received data structure

		Parameters
		----------
		value : (Any)
			the value that will be checked
		data_structure : (Iterable)
			a iterable in wich the received value is supposed to be present

		Raises
		----------
		ValidationError:
			if the value is not present in the data structure

		Returns
		________
		None
		'''

		if value not in data_structure:
			raise ValidationError(self.name, 'Value not present in the received data structure')

	def verify(self):
		pass


class StringValidator(Validator):
	'''
	A class to represent a string validator, children of Validator.

	...

	Methods
	-------
	email(value):
		Verify if the received value is a valid email address

	min(min, value):
		Verify if the length of the received value is equal or higher than the min

	max(max, value):
		Verify if the length of the received value is equal or lower than the max

	verify():
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method
	'''

	@validator
	def email(self, value: str) -> None:
		'''
		Verify if the received value is a valid email address

		Parameters
		----------
		value : (str)
			the value that will be checked

		Raises
		----------
		ValidationError:
			if the value is not a valid email address

		Returns
		________
		None
		'''

		if re.fullmatch(r'[^@]+@[^@]+\.[^@]+', value) is None:
			raise ValidationError(self.name, 'Value for email type does not match a valid format')

	@validator
	def min(self, min: int, value: str) -> None:
		'''
		Verify if the length of the received value is equal or higher than the min

		Parameters
		----------
		value : (str)
			the value that will be checked
		min : (int)
			the minimun length allowed

		Raises
		----------
		ValidationError:
			if the value length is smaller than the min

		Returns
		________
		None
		'''

		if len(value) < min:
			raise ValidationError(self.name, 'Value too short received')

	@validator
	def max(self, max: int, value: str) -> None:
		'''
		Verify if the length of the received value is equal or lower than the max

		Parameters
		----------
		value : (str)
			the value that will be checked
		max : (int)
			the maximun length allowed

		Raises
		----------
		ValidationError:
			if the value length is larger than the max

		Returns
		________
		None
		'''

		if len(value) > max:
			raise ValidationError(self.name, 'Value too long received')

	def verify(self) -> dict:
		'''
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method

		Returns
		-------
		result (str): The value returned by the input verify method
		'''

		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		if result is not None:
			result = str(result)

		result = self.input_.verify(result)
		return result


class NumericValidator(Validator):
	'''
	A class to represent a Numeric validator, children of Validator.

	...

	Methods
	-------
	min(min, value):
		Verify if the received value is equal or higher than the min

	max(max, value):
		Verify if the received value is equal or lower than the max

	verify():
		Get the validator's input value.
		If the value is not None converts it to a string and pass it to the input verify method
	'''

	@validator
	def min(self, min: int, value: decimal.Decimal) -> None:
		'''
		Verify if the received value is equal or higher than the min

		Parameters
		----------
		value : (any)
			the value that will be checked
		min : (int)
			the minimun value allowed

		Raises
		----------
		ValidationError:
			if the value smaller than the min

		Returns
		________
		None
		'''

		if value < min:
			raise ValidationError(self.name, 'Value too small received')

	@validator
	def max(self, max: int, value: decimal.Decimal) -> None:
		'''
		Verify if the the received value is equal or lower than the max

		Parameters
		----------
		value : (any)
			the value that will be checked
		max : (int)
			the maximun length allowed

		Raises
		----------
		ValidationError:
			if the value is larger than the max

		Returns
		________
		None
		'''

		if value > max:
			raise ValidationError(self.name, 'Value too large received')

	def verify(self) -> dict:
		'''
		Get the validator's input value, converts it to a Decimal and pass it to the input verify method

		Raises
		----------
		ValidationError:
			if the conversion operation to Decimal is invalid

		Returns
		-------
		result (Decimal): The value returned by the input verify method
		'''

		result = getattr(self.input_._input, self.input_._path)

		if callable(result):
			result = result()

		try:
			value = decimal.Decimal(result)
		except decimal.InvalidOperation:
			raise ValidationError(self.name, 'Non-numeric value received in a numeric input')

		return self.input_.verify(value)
