from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Collection, Product, Customer, Order, OrderItem
from tags.models import TaggedItem


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        return queryset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_title')
    list_editable = ('unit_price',)
    list_filter = ['collection', 'last_update', InventoryFilter,]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        prod_wording = 'product' if updated_count == 1 else 'products'
        aux_verb_wording = 'was' if updated_count == 1 else 'were'
        self.message_user(
            request,
            f'{updated_count} {prod_wording} {aux_verb_wording} successfully updated.',
            # messages.ERROR
            # messages.SUCCESS
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'membership')
    list_editable = ('membership',)
    list_per_page = 10
    ordering = ('first_name', 'last_name')
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'products_count')
    search_fields = ['title']

    # First implementation
    # @admin.display(ordering='products_count')
    # def products_count(self, collection):
    #     return collection.products_count

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
            # + urlencode({'collection_id': collection.id})    # This also works well
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(products_count=Count('product'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0
    min_num = 1
    max_num = 10


class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']


admin.site.register(Order, OrderAdmin)
