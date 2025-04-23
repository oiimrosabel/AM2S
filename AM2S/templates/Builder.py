from abc import abstractmethod


class Builder[T]:
	@abstractmethod
	def build(self) -> T:
		pass
