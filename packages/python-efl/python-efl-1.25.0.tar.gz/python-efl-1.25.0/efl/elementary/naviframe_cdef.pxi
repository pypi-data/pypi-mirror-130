cdef extern from "Elementary.h":
    ctypedef Eina_Bool (*Elm_Naviframe_Item_Pop_Cb)(void *data, Elm_Object_Item *it)

    Evas_Object             *elm_naviframe_add(Evas_Object *parent)
    Elm_Object_Item         *elm_naviframe_item_push(Evas_Object *obj, const char *title_label, Evas_Object *prev_btn, Evas_Object *next_btn, Evas_Object *content, const char *item_style)
    Elm_Object_Item         *elm_naviframe_item_insert_before(Evas_Object *obj, Elm_Object_Item *before, const char *title_label, Evas_Object *prev_btn, Evas_Object *next_btn, Evas_Object *content, const char *item_style)
    Elm_Object_Item         *elm_naviframe_item_insert_after(Evas_Object *obj, Elm_Object_Item *after, const char *title_label, Evas_Object *prev_btn, Evas_Object *next_btn, Evas_Object *content, const char *item_style)
    Evas_Object             *elm_naviframe_item_pop(Evas_Object *obj)
    void                     elm_naviframe_item_pop_to(Elm_Object_Item *it)
    void                     elm_naviframe_item_promote(Elm_Object_Item *it)
    void                     elm_naviframe_content_preserve_on_pop_set(Evas_Object *obj, Eina_Bool preserve)
    Eina_Bool                elm_naviframe_content_preserve_on_pop_get(const Evas_Object *obj)
    Elm_Object_Item         *elm_naviframe_top_item_get(const Evas_Object *obj)
    Elm_Object_Item         *elm_naviframe_bottom_item_get(const Evas_Object *obj)
    void                     elm_naviframe_item_style_set(Elm_Object_Item *it, const char *item_style)
    const char *             elm_naviframe_item_style_get(const Elm_Object_Item *it)
    void                     elm_naviframe_item_title_visible_set(Elm_Object_Item *it, Eina_Bool visible)
    Eina_Bool                elm_naviframe_item_title_visible_get(const Elm_Object_Item *it)
    void                     elm_naviframe_item_title_enabled_set(Elm_Object_Item *it, Eina_Bool enabled, Eina_Bool transition)
    Eina_Bool                elm_naviframe_item_title_enabled_get(const Elm_Object_Item *it)
    void                     elm_naviframe_prev_btn_auto_pushed_set(Evas_Object *obj, Eina_Bool auto_pushed)
    Eina_Bool                elm_naviframe_prev_btn_auto_pushed_get(const Evas_Object *obj)
    Eina_List               *elm_naviframe_items_get(const Evas_Object *obj)
    void                     elm_naviframe_event_enabled_set(Evas_Object *obj, Eina_Bool enabled)
    Eina_Bool                elm_naviframe_event_enabled_get(const Evas_Object *obj)
    Elm_Object_Item         *elm_naviframe_item_simple_push(Evas_Object *obj, Evas_Object *content)
    void                     elm_naviframe_item_simple_promote(Evas_Object *obj, Evas_Object *content)
    void                     elm_naviframe_item_pop_cb_set(Elm_Object_Item *it, Elm_Naviframe_Item_Pop_Cb func, void *data)
