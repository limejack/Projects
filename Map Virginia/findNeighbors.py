def dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
def compareNeighbors(a,b):
    for i in a:
        for j in b:
            if dist(i,j) < 5:
                return True

    return False
def getData(fileName):
    with open(fileName) as infile:
        data = infile.read().split('\n')[:-1]
    return [eval(i) for i in data]

counties = ['Lee County.txt', 'Scott County.txt', 'Wise County.txt', 'Norton City.txt', 'Russell County.txt', 'Washington County.txt', 'Bristol City.txt', 'Dickenson County.txt', 'Buchanan County.txt', 'Grayson County.txt', 'Smyth County.txt', 'Tazewell County.txt', 'Wythe County.txt', 'Bland County.txt', 'Galax City.txt', 'Carroll County.txt', 'Patrick County.txt', 'Pulaski County.txt', 'Floyd County.txt', 'Giles County.txt', 'Montgomery County.txt', 'Radford City.txt', 'Henry County.txt', 'Franklin County.txt', 'Roanoke County.txt', 'Salem City.txt', 'Martinsville City.txt', 'Pittsylvania County.txt', 'Roanoke City.txt', 'Bedford County.txt', 'Craig County.txt', 'Botetourt County.txt', 'Alleghany County.txt', 'Rockbridge County.txt', 'Covington City.txt', 'Bath County.txt', 'Highland County.txt', 'Danville City.txt', 'Halifax County.txt', 'Campbell County.txt', 'Mecklenburg County.txt', 'Charlotte County.txt', 'Appomattox County.txt', 'Prince Edward County.txt', 'Lynchburg City.txt', 'Amherst County.txt', 'Lexington City.txt', 'Buena Vista City.txt', 'Augusta County.txt', 'Nelson County.txt', 'Buckingham County.txt', 'Albemarle County.txt', 'Fluvanna County.txt', 'Lunenburg County.txt', 'Brunswick County.txt', 'Nottoway County.txt', 'Amelia County.txt', 'Greensville County.txt', 'Emporia City.txt', 'Sussex County.txt', 'Dinwiddie County.txt', 'Chesterfield County.txt', 'Petersburg City.txt', 'Farmville Town  Half PSAP.txt', 'Cumberland County.txt', 'Powhatan County.txt', 'Louisa County.txt', 'Goochland County.txt', 'Henrico County.txt', 'Richmond City.txt', 'Hanover County.txt', 'Caroline County.txt', 'Staunton City.txt', 'Rockingham County.txt', 'Waynesboro City.txt', 'Charlottesville City.txt', 'Greene County.txt', 'Harrisonburg City.txt', 'Shenandoah County.txt', 'Page County.txt', 'Frederick County.txt', 'Orange County.txt', 'Madison County.txt', 'Culpeper County.txt', 'Rappahannock County.txt', 'Culpeper Town.txt', 'Fauquier County.txt', 'Spotsylvania County.txt', 'Stafford County.txt', 'Fredericksburg City.txt', 'Prince William County.txt', 'Warren County.txt', 'Clarke County.txt', 'Winchester City.txt', 'Loudoun County.txt', 'Manassas City.txt', 'Manassas Park City.txt', 'Fairfax County.txt', 'Southampton County.txt', 'Franklin City.txt', 'Prince George County.txt', 'Colonial Heights City.txt', 'Surry County.txt', 'Suffolk City.txt', 'Isle of Wight County.txt', 'Chesapeake City.txt', 'James City County.txt', 'Newport News City.txt', 'Hampton City.txt', 'York County.txt', 'Hopewell City.txt', 'Charles City County.txt', 'New Kent County.txt', 'King William County.txt', 'King and Queen County.txt', 'Essex County.txt', 'Williamsburg City.txt', 'Gloucester County.txt', 'Middlesex County.txt', 'Mathews County.txt', 'Richmond County.txt', 'Lancaster County.txt', 'Northumberland County.txt', 'Portsmouth City.txt', 'Norfolk City.txt', 'Virginia Beach City.txt', 'Poquoson City.txt', 'Northampton County.txt', 'Accomack County.txt', 'King George County.txt', 'Westmoreland County.txt', 'Fairfax City.txt', 'Alexandria City.txt', 'Falls Church City.txt', 'Arlington County.txt']

neighbors = {}
for i in range(len(counties)):
    a = getData(counties[i])
    print('Starting '+counties[i])
    for j in range(i+1,len(counties)):
        b = getData(counties[j])
        if compareNeighbors(a,b):
            if counties[i] not in neighbors:
                neighbors[counties[i]] = []
            if counties[j] not in neighbors:
                neighbors[counties[j]] = []
            neighbors[counties[i]].append(counties[j])
            neighbors[counties[j]].append(counties[i])
    print('Finished '+counties[i])
