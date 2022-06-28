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


class Waiter(Employee):
    def __init__(self, name: str, work: str, profession: str, salary: int, work_experience: int):
        super().__init__(name, work, profession, salary)
        self.work_experience = work_experience


class Paleontologist(Employee):
    def __init__(self, name: str, work: str, profession: str, salary: int, work_experience: int):
        super().__init__(name, work, profession, salary)
        self.work_experience = work_experience

class Actor(Employee):
    def __init__(self, name: str, work: str, profession: str, salary: int, work_experience: int):
        super().__init__(name, work, profession, salary)
        self.work_experience = work_experience


class Work():
    def __init__(self, work, head: str, employees: list):
        self.work = work
        self.head = head
        self.employees = employees

    def __repr__(self):
        return f"The work place is located: {self.work}, street: {self.head} (total {len(self.employees)} employees)"

    def __iadd__(self, other):
        if isinstance(other, Employee):
            self.employees.append(other)
            return self
        else:
            raise TypeError("You can add only Employee class")

    def __isub__(self, other):
        if isinstance(other, Employee):
            self.employees.remove(other)
            return self
        else:
            raise TypeError("You can remove only Employee class")



class Organisation():
    def __init__(self, works: dict, vacancies: dict):
        self.works = works
        self.vacancies = vacancies

    def add_place(self, place):
        self.works[place.work] = place

    def intersection(self, other):
        return dict(set(self.vacancies.items()) & set(other.vacancies.items()))

    def union(self, other):
        return dict(set(self.vacancies.items()) | set(other.vacancies.items()))

    def __add__(self, other):
        return {k: self.vacancies.get(k, 0) + other.vacancies.get(k, 0) for k in set(self.vacancies) | set(other.vacancies)}

    def __sub__(self, other):
        return {k : other.vacancies[k] for k in set(other.vacancies) - set(self.vacancies)}

    def __repr__(self):
        return "Company:\n" + '\n'.join([str(f) for f in self.works])

emp_1 = Paleontologist('Ross Geller', 'Museum', 'paleontologist', 100000, 5)
emp_2 = Waiter('Chandler Bing', 'Central perk', 'waiter', 60000, 6)
emp_3 = Waiter('Rachel Green', 'Central perk', 'waiter', 70000, 3)
emp_4 = Actor('Joey Tribbiani', 'Cinema', 'actor',  70000, 4)
emp_5 = Paleontologist('Monica Geller', 'Museum', 'paleontologist', 90000, 7)
emp_6 = Waiter('Phoebe Buffay', 'Central perk','waiter',  100000, 9)


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
print(one + two)
print(one - two)
print(one == two)
print(one.union(two))
print()
one.add_place(work2)
print()
print(one.vacancies)
