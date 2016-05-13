from person import Person

class Population:
  def __init__(self, family_info, null_parent_value='0'):
    self.persons = {}

    # Initialize the persons data structure with Person objects
    for fid in family_info:
      self.persons[fid] = {}
      for iid in family_info[fid]:
        info = family_info[fid][iid]

        father_id = info['father_id']
        if father_id == null_parent_value:
          father_id = None

        mother_id = info['mother_id']
        if mother_id == null_parent_value:
          mother_id = None

        self.persons[fid][iid] = Person(fid, iid, father_id, mother_id, info['sex'], info['birthday'], info['datapresent'])

    # Create link structure between persons based on relationship
    for fid in self.persons:
      family_member_ids = self.persons[fid].keys()
      for iid in family_member_ids:
        person = self.persons[fid][iid]
        if person.father_id is not None:
          if person.father_id in family_member_ids:
            person.set_father(self.persons[fid][person.father_id])
            self.persons[fid][person.father_id].add_child(person)
          # else:
          #   print "%s's father %s is not in their family." % (person.iid, person.father_id)

        if person.mother_id is not None:
          if person.mother_id in family_member_ids:
            person.set_mother(self.persons[fid][person.mother_id])
            self.persons[fid][person.mother_id].add_child(person)
          # else:
          #   print "%s's mother %s is not in their family." % (person.iid, person.mother_id)
