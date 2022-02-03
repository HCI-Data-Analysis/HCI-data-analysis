class CourseSchema:
    CANCELLED_MODULES = [
        9
    ]

    OPTIONAL_MODULES = [
        11
    ]

    SUMMARY_MODULES = [
        10
    ]

    OPTIONAL_PAGES = {
        1: [6],
        2: [6],
        4: [11],
        6: [7],
        7: [7],
        8: [5],
        11: [1, 2, 3, 4, 5]  # All
    }

    OPTIONAL_PAGE_TITLES = [
        'interview'
    ]

    AVERAGE_READING_SPEED = 75

    MODULE_NUM_KEY = {
        741711: 0,
        741731: 1,
        741733: 2,
        741741: 3,
        741744: 4,
        741743: 5,
        741742: 6,
        741749: 7,
        741750: 8,
        741751: 9,
        741752: 10,
        741753: 11
    }

    OUTLIER_DATA448_IDS = [
        # TODO: add outlier student ids
    ]

    @staticmethod
    def page_is_valid(module_num: int, page_num: int) -> bool:
        if module_num in CourseSchema.CANCELLED_MODULES or \
                module_num in CourseSchema.OPTIONAL_MODULES or \
                module_num in CourseSchema.SUMMARY_MODULES:
            return False

        if module_num in CourseSchema.OPTIONAL_PAGES and \
                page_num in CourseSchema.OPTIONAL_PAGES[module_num]:
            return False

        return True
