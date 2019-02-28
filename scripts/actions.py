#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

BleedColor = "#ff0000"
BlockColor = "#0000ff"
DoesntUnlockColor = "#ffffff"
EquipColor = "#ffffff"
HuntColor = "#800517"
TorporColor = "#FF8040"
ReferendumColor = "#808080"
RecruitColor = "#00FFFF"
EmployColor = "#00FFFF"
MinionAbilityColor = "#FFFF00"
InterceptColor = "#0000ff"

BloodMarker = ("Blood counter", "044d5fe3-bdb5-4ad2-5fa4-000000000025")
LifeMarker = ("Life counter", "170ab056-46d4-477c-81d8-66529974aa54")
AddMarker = ("counter", "0809c9b7-5407-4266-899f-b7cadf417091")


#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------

def endTurn(args):
    mute()
    player = args.player
    if player == me:
        clearAll(table, x = 0, y = 0)

def changePhase(args):
    mute()
    phaseIdx = currentPhase()[1]
    if phaseIdx == 1 and me.isActive:
        goToUnlock(table)

lastDrawnCard = 0

#---------------------------------------------------------------------------
# Table group actions
#---------------------------------------------------------------------------

def react(group, x = 0, y = 0):
    notify('{} will react!'.format(me))

def noreact(group, x = 0, y = 0):
    notify('{} doesn\'t react.'.format(me))

def scoop(group, x = 0, y = 0):
    mute()
    if not confirm("Are you sure you want to scoop?"): return
    me.pool = 30
    me.VPs = 0
    myCards = (card for card in table
                    if card.owner == me)
    for card in myCards: 
        card.moveTo(me.piles['Library'])
    Library = me.piles['Library']
    for c in me.piles['Ash Heap']: c.moveTo(Library)
    for c in me.hand: c.moveTo(Library)
    exile = me.piles['Removed from game']
    for c in exile: c.moveTo(Library)
    notify("{} scoops.".format(me))

def showCurrentPhase(group, x = 0, y = 0):
    notify(phases[phaseIdx].format(me))

def nextPhase(group, x = 0, y = 0):
    mute()
    phaseIdx = currentPhase()[1]
    if phaseIdx == 5:
        setPhase(0)
    else:
        setPhase(phaseIdx + 1)

def goToUnlock(group, x = 0, y = 0):
    mute()
    myCards = (card for card in table
                    if card.controller == me
                    and card.highlight != DoesntUnlockColor)
    for card in myCards: 
        card.orientation &= ~Rot90
    notify("{} unlocks and enters in UNLOCK Phase.".format(me))

def goToMaster(group, x = 0, y = 0):
    setPhase(2)
    showCurrentPhase(group)

def goToMinion(group, x = 0, y = 0):
    setPhase(3)
    showCurrentPhase(group)

def goToInfluence(group, x = 0, y = 0):
    setPhase(4)
    showCurrentPhase(group)

def goToDiscard(group, x = 0, y = 0):
    setPhase(5)
    showCurrentPhase(group)

def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def roll20(group, x = 0, y = 0):
    mute()
    n = rnd(1, 20)
    notify("{} rolls {} on a 20-sided die.".format(me, n))

def flipCoin(group, x = 0, y = 0):
    mute()
    n = rnd(1, 2)
    if n == 1:
        notify("{} flips heads.".format(me))
    else:
        notify("{} flips tails.".format(me))

def token(group, x = 0, y = 0):
    card, quantity = askCard({"Type":"Token"}, "And")
    if quantity == 0: return
    table.create(card, x, y, quantity)

def align(group, x = 0, y = 0):
  mute()
  text = cardalign()
  notify("{} re-aligns his cards on the table".format(me))

def clearAll(group, x = 0, y = 0):
    notify("{} clears all targets and highlights.".format(me))
    for card in group:
      card.target(False)
      if card.controller == me:
          card.highlight = None		  

def rulings(group, x = 0, y = 0):
  mute()
  openUrl('http://www.vekn.net/index.php/card-rulings')
  notify('{} is checking card rulings on vekn.net.'.format(me))

#---------------------------------------------------------------------------
# Table card actions
#---------------------------------------------------------------------------

def deplete(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} locks {}'.format(me, card))
    else:
        notify('{} unlocks {}'.format(me, card))

def doesNotUnlock(card, x = 0, y = 0):
    if card.highlight == DoesntUnlockColor:
        card.highlight = None
        notify("{0}'s {1} can now unlock.".format(me, card))
    else:
        card.highlight = DoesntUnlockColor
        notify("{0}'s {1} will not unlock.".format(me, card))

def contest(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot180
    if card.orientation & Rot180 == Rot180:
        notify('{} contest {}'.format(me, card))
    else:
        notify('{} unflips {}'.format(me, card))

def ability(card, x = 0, y = 0):
    mute()
    card.highlight = MinionAbilityColor
    notify("{} uses {}'s ability".format(me, card))

def bleed(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = BleedColor
    notify('{} bleeds with {}'.format(me, card))

def equip(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = EquipColor
    notify('{} equips with {}'.format(me, card))

def hunt(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = HuntColor
    notify('{} hunts with {}'.format(me, card))

def torporleave(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = TorporColor
    notify('{} leaves torpor with {}'.format(me, card))

def torporrescue(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = TorporColor
    notify('{} rescues from torpor with {}'.format(me, card))

def referendum(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = ReferendumColor
    notify('{} calls a referendum with {}'.format(me, card))

def recruit(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = RecruitColor
    notify('{} recuits with {}'.format(me, card))

def employ(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = EmployColor
    notify('{} employs with {}'.format(me, card))

def becomeanarch(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = MinionAbilityColor
    notify('{} becomes a anarch with {}'.format(me, card))

def intercept(card, x = 0, y = 0):
    mute()
    card.orientation |= Rot90
    card.highlight = InterceptColor
    notify('{} adds intercepts with {}'.format(me, card))

def trytoblock(card, x = 0, y = 0):
    mute()
    card.highlight = BlockColor
    notify('{} try to block with {}'.format(me, card))

def Intercept1(card, x = 0, y = 0):
    mute()
    card.highlight = BlockColor
    notify('{} try to block with +1 intercept with {}'.format(me, card))

def Intercept2(card, x = 0, y = 0):
    mute()
    card.highlight = BlockColor
    notify('{} try to block with +2 intercept with {}'.format(me, card))

def change(card, x = 0, y = 0):
    mute()
    card.highlight = BleedColor
    notify('{} redirect bleeds with {}'.format(me, card))

def noblock(group, x = 0, y = 0):
    notify('{} doesn\'t try to block'.format(me))

def addmarker(cards, x = 0, y = 0):
    mute()
    marker, quantity = askMarker()
    if quantity == 0:
        return
    for card in cards:
        card.markers[marker] += quantity
        notify("{} adds {} {} counters to {}.".format(me, quantity, marker[0], card))

def addbloodcounter(card, x = 0, y = 0):
 mute()
 notify("{} adds a blood counter to {}.".format(me, card))
 card.markers[BloodMarker] += 1

def addxbloodcounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Add how many blood?", 0)
 if count == None: return
 card.markers[BloodMarker] += count 
 notify("{} adds {} blood counter(s) to {}.".format(me, count, card))

def transferbloodcounter(card, x = 0, y = 0):
 mute()
 card.markers[BloodMarker] += 1
 me.pool -= 1
 notify("{} transfer a blood counter from their pool to {}.".format(me, card))

def transferxbloodcounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Add how many blood?", 0)
 if count == None: return
 card.markers[BloodMarker] += count
 me.pool -= count
 notify("{} transfers {} blood counter(s) from their pool to {}.".format(me, count, card))

def transferlifecounter(card, x = 0, y = 0):
 mute()
 card.markers[LifeMarker] += 1
 me.pool -= 1
 notify("{} transfer a life counter from their pool to {}.".format(me, card))

def transferxlifecounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Add how many life?", 0)
 if count == None: return
 card.markers[LifeMarker] += count
 me.pool -= count
 notify("{} transfers {} life counter(s) from their pool to {}.".format(me, count, card))

def addlifecounter(card, x = 0, y = 0):
 mute()
 notify("{} adds a life counter to {}.".format(me, card))
 card.markers[LifeMarker] += 1

def addxlifecounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Add how many life?", 0)
 if count == None: return
 card.markers[LifeMarker] += count
 notify("{} adds {} life counter(s) to {}.".format(me, count, card))

def addcounter(card, x = 0, y = 0):
 mute()
 notify("{} adds a generic counter to {}.".format(me, card))
 card.markers[AddMarker] += 1

def paycontestblood(card, x = 0, y = 0):
 mute()
 notify("{} burn a blood counter from {} to pay title contest.".format(me, card))
 card.markers[BloodMarker] -= 1
 
def paycontestpool(card, x = 0, y = 0):
 mute()
 notify("{} burn a pool to pay {} contest.".format(me, card))
 me.pool -= 1

def yieldcontest(card, x = 0, y = 0):
 mute()
 notify("{} yield contest of {}.".format(me, card))

def removebloodcounter(card, x = 0, y = 0):
 mute()
 notify("{} removes a blood counter from {}.".format(me, card))
 card.markers[BloodMarker] -= 1

def removexbloodcounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Remove how many blood?", 0)
 if count == None: return
 card.markers[BloodMarker] -= count
 notify("{} removes {} blood counter(s) from {}.".format(me, count, card))
 
def removelifecounter(card, x = 0, y = 0):
 mute()
 notify("{} removes a life counter from {}.".format(me, card))
 card.markers[LifeMarker] -= 1

def removexlifecounter(card, x = 0, y = 0):
 mute()
 count = askInteger("Remove how many life?", 0)
 if count == None: return
 card.markers[LifeMarker] -= count
 notify("{} removes {} life counter(s) from {}.".format(me, count, card))

def removegenericcounter(card, x = 0, y = 0):
 mute()
 notify("{} removes a generic counter from {}.".format(me, card))
 card.markers[AddMarker] -= 1

def turn(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        notify("{} turns {} face down.".format(me, card))
        card.isFaceUp = False
    else:
        card.isFaceUp = True
        notify("{} turns {} face up.".format(me, card))

def clear(card, x = 0, y = 0):
 notify("{} clears {}.".format(me, card))
 card.highlight = None
 card.target(False)


#---------------------------
#movement actions
#---------------------------

def destroy(card, x = 0, y = 0):
 mute()
 card.moveTo(me.piles['Ash Heap'])
 notify("{} burns {}.".format(me, card))

def removefromgame(card, x = 0, y = 0):
 mute()
 notify("{} removes {} from game.".format(me, card))
 card.moveTo(me.piles['Removed from game'])

def movetodrawdeck(card, x = 0, y = 0):
    mute()
    card.moveTo(me.piles['draw deck'])
    notify("{} moves {} to top of draw deck.".format(me, card))

def tohand(card, x = 0, y = 0):
 mute()
 src = card.group
 fromText = " from the table" if src == table else " from their " + src.name
 card.moveTo(me.hand)
 notify("{} returns {} to their hand{}.".format(me, card.name, fromText))

def movetobottom(card, x = 0, y = 0):
 card.moveToBottom(me.pile['draw deck'])



#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def play(card, x = 0, y = 0):
 mute()
 src = card.group
 card.moveToTable(0, 0)
 notify("{} plays {} from their {}.".format(me, card, src.name))

def randomDiscard(group):
 mute()
 card = group.random()
 if card == None: return
 notify("{} randomly discards a {}.".format(me, card))
 card.moveTo(me.piles['Ash Heap'])

def discard(card, x = 0, y = 0):
 mute()
 notify("{} discards {} from their hand.".format(me, card))
 card.moveTo(me.piles['Ash Heap'])
 
def discardx(group):
 if len(group) == 0: return
 mute()
 count = askInteger("How many cards to discard?", 0)
 if count == None: return
 for c in group.top(count): c.moveTo(me.piles['Ash Heap'])
 notify("{} discards {} card(s) from their library.".format(me, count))
 
def removefromgame(card, x = 0, y = 0):
 mute()
 notify("{} removes {} from game.".format(me, card))
 card.moveTo(me.piles['Removed from game'])
 
def removex(group):
 if len(group) == 0: return
 mute()
 count = askInteger("How many cards to remove from game?", 0)
 if count == None: return
 for c in group.top(count): c.moveTo(me.piles['Removed from game'])
 notify("{} removes from the game {} card(s) from their ash heap.".format(me, count))
 
def librarytop(card, x = 0, y = 0):
 mute()
 card.moveTo(me.piles['Library'])
 notify("{} moves a card from their Hand to top of library.".format(me))

def librarybotton(card, x = 0, y = 0):
 mute()
 card.moveToBottom(me.piles['Library'])
 notify("{} moves a card from their Hand to botton of library.".format(me))

#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------

def draw(group, x = 0, y = 0):
 if len(group) == 0: return
 mute()
 group[0].moveTo(me.hand)
 notify("{} draws a card.".format(me))

def shuffle(group):
  group.shuffle()

def drawMany(group):
 if len(group) == 0: return
 mute()
 count = askInteger("Draw how many cards?", 7)
 if count == None: return
 for c in group.top(count): c.moveTo(me.hand)
 notify("{} draws {} cards.".format(me, count))
 
def undoDraw(group=None, x=0, y=0):
    mute()
    global lastDrawnCard
    if lastDrawnCard == None:
        whisper("There was a problem undoing drawing a card.")
        return
	Library = me.piles['Library']
    lastDrawnCard.moveTo(me.piles['Library'])
    lastDrawnCard = None
    notify("{} undoes drawing a card from Library.".format(me))

def revealtoplibrary(group, x = 0, y = 0):
    mute()
    if group[0].isFaceUp:
        notify("{} hides {} from the top of their library.".format(me, group[0]))
        group[0].isFaceUp = False
    else:
        group[0].isFaceUp = True
        notify("{} reveals {} from the top of their library.".format(me, group[0]))

def revealtopcrypt(group, x = 0, y = 0):
    mute()
    if group[0].isFaceUp:
        notify("{} hides {} from the top of their crypt.".format(me, group[0]))
        group[0].isFaceUp = False
    else:
        group[0].isFaceUp = True
        notify("{} reveals {} from the top of their crypt.".format(me, group[0]))

def drawCrypt(card, x = 0, y = 0):
 mute()
 card.moveToTable(0, 0, True)
 notify("{} draws a crypt card.".format(me))

def randomdraw(group):
 mute()
 card = group.random()
 if card == None: return
 notify("{} randomly draws a card.".format(me))
 card.moveTo(me.hand)
 
#------------------------------------------------------------------------------
# Events
#------------------------------------------------------------------------------ 
 
 def changePhase(args):
    mute()
    phaseIdx = currentPhase()[1]
    if phaseIdx == 1 and me.isActive:
        goToUnlock(table)

#------------------------------------------------------------------------------
# Responses
#------------------------------------------------------------------------------

def response(group, x = 0, y = 0):
    notify('{} burns the EDGE for a vote in favor'.format(me))

def response1(group, x = 0, y = 0):
    notify('{} burn the EDGE for a vote against!'.format(me))

def response2(group, x = 0, y = 0):
    notify('{} burns a political card from hand for a vote in favor'.format(me))

def response3(group, x = 0, y = 0):
    notify('{} burns a political card from hand for a vote against'.format(me))

def response4(group, x = 0, y = 0):
    notify('{} has no votes or abstens from this referendum'.format(me))

def response6(group, x = 0, y = 0):
    notify('Start Combat'.format(me))

def response7(group, x = 0, y = 0):
    notify('{} has no pre manuever'.format(me))

def response8(group, x = 0, y = 0):
    notify('{} has no manuever'.format(me))

def response9(group, x = 0, y = 0):
    notify('{} manuevers to long range'.format(me))

def response10(group, x = 0, y = 0):
    notify('{} manuevers to close range'.format(me))

def response11(group, x = 0, y = 0):
    notify('{} has no pre strike'.format(me))

def response12(group, x = 0, y = 0):
    notify('{} strikes with hand damage'.format(me))

def response13(group, x = 0, y = 0):
    notify('{} has no additional strikes'.format(me))

def response14(group, x = 0, y = 0):
    notify('{} has additional strike'.format(me))

def response15(group, x = 0, y = 0):
    notify('{} has two additional strikes'.format(me))

def response16(group, x = 0, y = 0):
    mute()
    count = askInteger("How many strikes?", 0)
    if count == None: return 
    notify('{} has {} additional strike(s)'.format(me, count))

def response17(group, x = 0, y = 0):
    notify('{} has no press'.format(me))

def response18(group, x = 0, y = 0):
    notify('{} presses to continue combat'.format(me))

def response19(group, x = 0, y = 0):
    notify('{} presses to end combat'.format(me))

def response20(group, x = 0, y = 0):
    notify('{} start new round of combat'.format(me))

def response21(group, x = 0, y = 0):
    notify('{} ends combat'.format(me))

def response22(group, x = 0, y = 0):
    notify('{} restarts combat'.format(me))

def response23(group, x = 0, y = 0):
    mute()
    count = askInteger("How many votes for?", 0)
    if count == None: return 
    notify('{} has a total of {} vote(s) for in this referendum '.format(me, count))

def response24(group, x = 0, y = 0):
    mute()
    count = askInteger("How many votes against?", 0)
    if count == None: return 
    notify('{} has a total of {} vote(s) against in this referendum '.format(me, count))