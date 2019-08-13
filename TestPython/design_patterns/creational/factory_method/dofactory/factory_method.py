__author__ = 'R.Azh'

# Define an interface for creating an object,
#  but let subclasses decide which class to instantiate.
# Factory Method lets a class defer instantiation to subclasses.


# Product: defines the interface of objects the factory method creates
class Page:
    pass


# ConcreteProduct: implements the Product interface
class SkillsPage(Page):
    pass


# ConcreteProduct
class EducationPage(Page):
    pass


# ConcreteProduct
class ExperiencePage(Page):
    pass


# ConcreteProduct
class IntroductionPage(Page):
    pass


# ConcreteProduct
class ResultsPage(Page):
    pass


# ConcreteProduct
class ConclusionPage(Page):
    pass


# ConcreteProduct
class SummaryPage(Page):
    pass


# ConcreteProduct
class BibliographyPage(Page):
    pass


# Creator: declares the factory method, which returns an object of type Product. Creator may also define a default
# implementation of the factory method that returns a default ConcreteProduct object.
# may call the factory method to create a Product object.
class Document:
    _pages = None

    def __init__(self):
        self._pages = []
        self.create_pages()

    def create_pages(self):
        raise NotImplementedError()

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        self._pages = value

    def __str__(self):
        return " ".join(page.__name__ for page in self._pages)


# ConcreteCreator: overrides the factory method to return an instance of a ConcreteProduct.
class Resume(Document):
    def create_pages(self):
        super().pages.append(SkillsPage)
        super().pages.append(EducationPage)
        super().pages.append(ExperiencePage)


# ConcreteCreator
class Report(Document):
    def create_pages(self):
        super().pages.append(IntroductionPage)
        super().pages.append(ResultsPage)
        super().pages.append(ConclusionPage)
        super().pages.append(SummaryPage)
        super().pages.append(BibliographyPage)


######### usage ###########

documents = []
documents.append(Resume())
documents.append(Report())

for document in documents:
    print("\n__", type(document).__name__, "__")
    for page in document.pages:
        print(" ", page.__name__)
    #     or
    print(document)