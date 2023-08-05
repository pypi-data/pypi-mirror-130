cdef extern from "Edje.h":
    ####################################################################
    # Enums
    #
    ctypedef enum Edje_Message_Type:
        EDJE_MESSAGE_NONE
        EDJE_MESSAGE_SIGNAL
        EDJE_MESSAGE_STRING
        EDJE_MESSAGE_INT
        EDJE_MESSAGE_FLOAT
        EDJE_MESSAGE_STRING_SET
        EDJE_MESSAGE_INT_SET
        EDJE_MESSAGE_FLOAT_SET
        EDJE_MESSAGE_STRING_INT
        EDJE_MESSAGE_STRING_FLOAT
        EDJE_MESSAGE_STRING_INT_SET
        EDJE_MESSAGE_STRING_FLOAT_SET

    ctypedef enum Edje_Aspect_Control:
        EDJE_ASPECT_CONTROL_NONE
        EDJE_ASPECT_CONTROL_NEITHER
        EDJE_ASPECT_CONTROL_HORIZONTAL
        EDJE_ASPECT_CONTROL_VERTICAL
        EDJE_ASPECT_CONTROL_BOTH

    ctypedef enum Edje_Drag_Dir:
        EDJE_DRAG_DIR_NONE
        EDJE_DRAG_DIR_X
        EDJE_DRAG_DIR_Y
        EDJE_DRAG_DIR_XY

    ctypedef enum Edje_Load_Error:
        EDJE_LOAD_ERROR_NONE
        EDJE_LOAD_ERROR_GENERIC
        EDJE_LOAD_ERROR_DOES_NOT_EXIST
        EDJE_LOAD_ERROR_PERMISSION_DENIED
        EDJE_LOAD_ERROR_RESOURCE_ALLOCATION_FAILED
        EDJE_LOAD_ERROR_CORRUPT_FILE
        EDJE_LOAD_ERROR_UNKNOWN_FORMAT
        EDJE_LOAD_ERROR_INCOMPATIBLE_FILE
        EDJE_LOAD_ERROR_UNKNOWN_COLLECTION
        EDJE_LOAD_ERROR_RECURSIVE_REFERENCE

    ctypedef enum Edje_Part_Type:
        EDJE_PART_TYPE_NONE
        EDJE_PART_TYPE_RECTANGLE
        EDJE_PART_TYPE_TEXT
        EDJE_PART_TYPE_IMAGE
        EDJE_PART_TYPE_SWALLOW
        EDJE_PART_TYPE_TEXTBLOCK
        EDJE_PART_TYPE_GRADIENT
        EDJE_PART_TYPE_GROUP
        EDJE_PART_TYPE_BOX
        EDJE_PART_TYPE_TABLE
        EDJE_PART_TYPE_EXTERNAL
        EDJE_PART_TYPE_SPACER
        EDJE_PART_TYPE_MESH_NODE
        EDJE_PART_TYPE_LIGHT
        EDJE_PART_TYPE_CAMERA
        EDJE_PART_TYPE_LAST

    ctypedef enum Edje_Text_Effect:
        EDJE_TEXT_EFFECT_NONE
        EDJE_TEXT_EFFECT_PLAIN
        EDJE_TEXT_EFFECT_OUTLINE
        EDJE_TEXT_EFFECT_SOFT_OUTLINE
        EDJE_TEXT_EFFECT_SHADOW
        EDJE_TEXT_EFFECT_SOFT_SHADOW
        EDJE_TEXT_EFFECT_OUTLINE_SHADOW
        EDJE_TEXT_EFFECT_OUTLINE_SOFT_SHADOW
        EDJE_TEXT_EFFECT_FAR_SHADOW
        EDJE_TEXT_EFFECT_FAR_SOFT_SHADOW
        EDJE_TEXT_EFFECT_GLOW
        EDJE_TEXT_EFFECT_LAST
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_BOTTOM_RIGHT
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_BOTTOM
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_BOTTOM_LEFT
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_LEFT
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_TOP_LEFT
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_TOP
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_TOP_RIGHT
        EDJE_TEXT_EFFECT_SHADOW_DIRECTION_RIGHT

    ctypedef enum Edje_Action_Type:
        EDJE_ACTION_TYPE_NONE
        EDJE_ACTION_TYPE_STATE_SET
        EDJE_ACTION_TYPE_ACTION_STOP
        EDJE_ACTION_TYPE_SIGNAL_EMIT
        EDJE_ACTION_TYPE_DRAG_VAL_SET
        EDJE_ACTION_TYPE_DRAG_VAL_STEP
        EDJE_ACTION_TYPE_DRAG_VAL_PAGE
        EDJE_ACTION_TYPE_SCRIPT
        EDJE_ACTION_TYPE_FOCUS_SET
        EDJE_ACTION_TYPE_RESERVED00
        EDJE_ACTION_TYPE_FOCUS_OBJECT
        EDJE_ACTION_TYPE_PARAM_COPY
        EDJE_ACTION_TYPE_PARAM_SET
        EDJE_ACTION_TYPE_SOUND_SAMPLE
        EDJE_ACTION_TYPE_SOUND_TONE
        EDJE_ACTION_TYPE_PHYSICS_IMPULSE
        EDJE_ACTION_TYPE_PHYSICS_TORQUE_IMPULSE
        EDJE_ACTION_TYPE_PHYSICS_FORCE
        EDJE_ACTION_TYPE_PHYSICS_TORQUE
        EDJE_ACTION_TYPE_PHYSICS_FORCES_CLEAR
        EDJE_ACTION_TYPE_PHYSICS_VEL_SET
        EDJE_ACTION_TYPE_PHYSICS_ANG_VEL_SET
        EDJE_ACTION_TYPE_PHYSICS_STOP
        EDJE_ACTION_TYPE_PHYSICS_ROT_SET
        EDJE_ACTION_TYPE_VIBRATION_SAMPLE
        EDJE_ACTION_TYPE_LAST

    ctypedef enum Edje_Tween_Mode:
        EDJE_TWEEN_MODE_NONE
        EDJE_TWEEN_MODE_LINEAR
        EDJE_TWEEN_MODE_SINUSOIDAL
        EDJE_TWEEN_MODE_ACCELERATE
        EDJE_TWEEN_MODE_DECELERATE
        EDJE_TWEEN_MODE_ACCELERATE_FACTOR
        EDJE_TWEEN_MODE_DECELERATE_FACTOR
        EDJE_TWEEN_MODE_SINUSOIDAL_FACTOR
        EDJE_TWEEN_MODE_DIVISOR_INTERP
        EDJE_TWEEN_MODE_BOUNCE
        EDJE_TWEEN_MODE_SPRING
        EDJE_TWEEN_MODE_CUBIC_BEZIER
        EDJE_TWEEN_MODE_LAST
        EDJE_TWEEN_MODE_MASK
        EDJE_TWEEN_MODE_OPT_FROM_CURRENT

    ctypedef enum Edje_External_Param_Type:
        EDJE_EXTERNAL_PARAM_TYPE_INT
        EDJE_EXTERNAL_PARAM_TYPE_DOUBLE
        EDJE_EXTERNAL_PARAM_TYPE_STRING
        EDJE_EXTERNAL_PARAM_TYPE_BOOL
        EDJE_EXTERNAL_PARAM_TYPE_CHOICE
        EDJE_EXTERNAL_PARAM_TYPE_MAX

    ctypedef enum Edje_Input_Hints:
        EDJE_INPUT_HINT_NONE
        EDJE_INPUT_HINT_AUTO_COMPLETE
        EDJE_INPUT_HINT_SENSITIVE_DATA
