class CategoriesParser():
    def __init__(self, content):
        self.content = content

    def parse_google(self):
        # for raw format see https://www.google.com/basepages/producttype/taxonomy-with-ids.en-GB.txt
        new_list = self.content.decode().split('\n')[1:-1] # we don't want the first and last lines
        categories_parsed = []
        for category_unparsed in new_list:
            category_parts = category_unparsed.split(' - ')
            categories_parsed.append({
                'id': category_parts[0],
                'categories': category_parts[1].split(' > ')
            })

        return categories_parsed