
RUNELITE = True

SIDEBAR_ON = True

if RUNELITE and SIDEBAR_ON:
    INVENTORY_X1 = 1231
    INVENTORY_Y1 = 576

    # inv#1 bottom right = Point(x=1284, y=623)
    INVENTORY_X2 = 1284
    INVENTORY_Y2 = 623

    ITEM_WIDTH = INVENTORY_X2 - INVENTORY_X1
    ITEM_HEIGHT = INVENTORY_Y2 - INVENTORY_Y1

    SLOTS_HORIZONTAL = 4
    SLOTS_VERTICAL = 7

    # inv#2 top left = Point(x=1294, y=576)
    INVENTORY_X_GAP = 10

    # inv#5 top left = Point(x=1231, y=630)
    INVENTORY_Y_GAP = 7
