names = ["Zhanasyl", "Aizere", "Magzhan", "Javier", "Alex", "Marzhan"]

m_names = list(filter(lambda x : x[0].lower() == "m", names))
print(m_names)

a_names = list(filter(lambda x : x[0].lower() == "a", names))
print(a_names)