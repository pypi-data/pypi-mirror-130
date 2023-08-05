cdef extern from "Elementary.h":
    Evas_Object             *elm_player_add(Evas_Object *parent)
    Evas_Object             *elm_video_add(Evas_Object *parent)
    Eina_Bool                elm_video_file_set(Evas_Object *video, const char *filename)
    void                     elm_video_file_get(Evas_Object *video, const char **filename)
    Evas_Object             *elm_video_emotion_get(const Evas_Object *video)
    void                     elm_video_play(Evas_Object *video)
    void                     elm_video_pause(Evas_Object *video)
    void                     elm_video_stop(Evas_Object *video)
    Eina_Bool                elm_video_is_playing_get(const Evas_Object *video)
    Eina_Bool                elm_video_is_seekable_get(const Evas_Object *video)
    Eina_Bool                elm_video_audio_mute_get(const Evas_Object *video)
    void                     elm_video_audio_mute_set(Evas_Object *video, Eina_Bool mute)
    double                   elm_video_audio_level_get(const Evas_Object *video)
    void                     elm_video_audio_level_set(Evas_Object *video, double volume)
    double                   elm_video_play_position_get(const Evas_Object *video)
    void                     elm_video_play_position_set(Evas_Object *video, double position)
    double                   elm_video_play_length_get(const Evas_Object *video)
    void                     elm_video_remember_position_set(Evas_Object *video, Eina_Bool remember)
    Eina_Bool                elm_video_remember_position_get(const Evas_Object *video)
    const char *             elm_video_title_get(const Evas_Object *video)
