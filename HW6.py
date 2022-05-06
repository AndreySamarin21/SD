class Employee():

    num_of_emp = 0

    def __init__(self, name: str, work: str, profession: str, salary: int):
        self.name = name
        self.work = work
        self.profession = profession
        self.salary = salary

        Employee.num_of_emp += 1

    def __str__(self):
        return f"{self.name} from {self.work} dep, {self.profession}"



class Work():
    def __init__(self, work, head: str, employees: list):
        self.work = work
        self.head = head
        self.employees = employees

    def __repr__(self):
        return f"The work place is located: {self.work}, street: {self.head} (total {len(self.employees)} employees)"


class Organisation():
    def __init__(self, works: dict, vacancies: dict):
        self.works = works
        self.vacancies = vacancies

    def add_dep(self, dep):
        self.works[dep.work] = dep

    def intersection(self, other):
        return dict(set(self.vacancies.items()) & set(other.vacancies.items()))

    def union(self, other):
        return dict(set(self.vacancies.items()) | set(other.vacancies.items()))

    def __add__(self, other):
        return {k: self.vacancies.get(k, 0) + other.vacancies.get(k, 0) for k in set(self.vacancies) | set(other.vacancies)}

    def __sub__(self, other):
        return { k : other.vacancies[k] for k in set(other.vacancies) - set(self.vacancies) }

emp_1 = Employee('Ross Geller', 'Museum', 'paleontologist', 100000)
emp_2 = Employee('Chandler Bing', 'Central perk', 'waiter', 60000)
emp_3 = Employee('Rachel Green', 'Central perk', 'waiter', 70000)
emp_4 = Employee('Joey Tribbiani', 'Cinema', 'actor',  70000)
emp_5 = Employee('Monica Geller', 'Museum', 'paleontologist', 90000)
emp_6 = Employee('Phoebe Buffay', 'Central perk','waiter',  100000)


vacancies1 = {"waiter": 2, "paleontologist": 0}
vacancies2 = {"waiter": 2, "actor": 1}

work1 = Work('Las Vegas', "Festival Grounds", [emp_1, emp_2, emp_3])
work2 = Work('New York', "Manhattan", [emp_4, emp_5, emp_6])


one = Organisation({work1.work: work1}, vacancies1)

two = Organisation({work1.work: work2}, vacancies2)

print(f'Total added {Employee.num_of_emp} employees')
print()
print(one.union(two))
print(one.intersection(two))

print(one == two)
print(one.union(two))
print(one + two)
print(one - two)
print()
one.add_dep(work2)
