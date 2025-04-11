# 常量
JWT_TOKEN_EXPIRE_HOURS = 1  # JWT 过期时间(单位：小时)
FEEDBACK_HANDLE_STATUS_PROCESSED = 1 # 反馈处理状态：已处理
FEEDBACK_HANDLE_STATUS_REVOKE = 2 # 反馈处理状态：撤销


# 用户关注关系
USER_FOLLOW_STATUS_FOLLOWED = 1  # 用户关注状态：已关注
USER_FOLLOW_STATUS_UNFOLLOWED = 2  # 用户关注状态：未关注
USER_FOLLOW_STATUS_MUTUAL = 3  # 用户关注状态：互相关注
USER_FOLLOW_STATUS_FOLLOWBACK = 4  # 用户关注状态：待回关（客体已关注主体，但主体未关注客体）


# 分页设置
PAGE_SIZE = 10  # 每页显示条数

IMAGE_UPLOAD_PATH =  "/uploads/images"  # 图片上传路径
VIDEO_UPLOAD_PATH = "/uploads/videos"  # 视频上传路径
