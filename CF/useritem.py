import numpy as np
import pandas as pd


# 定义初始化参数函数
# 输入：特征数量、用户数量、产品数量
# 输出：用户特征初始矩阵、产品特征初始矩阵
def Initialize_Parameters(num_features, num_users, num_products):
    user_matrix = np.random.rand(num_users, num_features)
    product_matrix = np.random.rand(num_products, num_features)
    return user_matrix, product_matrix


# 计算当前的代价函数
# 输入：当前的用户矩阵、产品矩阵、缺失的二维表、惩罚因子 lambdaa
# 输出：当前代价
def get_cost(ori_data, user_matrix, product_matrix, lambdaa):
    nan_index = np.isnan(ori_data)  # 记录二维表中缺失的索引
    ori_data[nan_index] = 0  # 把缺失值填充为 0
    predict_data = np.dot(user_matrix, product_matrix.T)  # 计算预测的评分
    temp = predict_data - ori_data  # 计算两矩阵的差值
    temp[nan_index] = 0  # 缺失值不算在代价里
    cost = 0.5 * np.sum(temp ** 2) + 0.5 * lambdaa * (np.sum(user_matrix ** 2) + np.sum(product_matrix ** 2))  # 计算平方
    ori_data[nan_index] = np.nan  # 恢复原数据

    return cost


# 对用户特征进行偏导
# 输入：当前的用户矩阵、产品矩阵、缺失的二维表、惩罚因子 lambdaa、加权平均参数
# 输出：用户特征偏导矩阵、加权平均矩阵
def get_user_derivatives(ori_data, user_matrix, product_matrix, weight_average_matrix, lambdaa=1,
                         weight_average_para=0):
    nan_index = np.isnan(ori_data)  # 记录二维表中缺失的索引
    ori_data[nan_index] = 0  # 把缺失值填充为 0
    predict_data = np.dot(user_matrix, product_matrix.T)  # 计算预测的评分
    temp = predict_data - ori_data  # 计算两矩阵的差值
    temp[nan_index] = 0  # 缺失值不算在代价里
    ori_data[nan_index] = np.nan  # 恢复原数据

    num_user = user_matrix.shape[0]  # 计算用户数目
    feature_user = user_matrix.shape[1]  # 计算特征数目
    user_dervatives = np.random.rand(num_user, feature_user)  # 声明用户特征偏导数矩阵

    for i in range(num_user):
        for j in range(feature_user):
            user_dervatives[i][j] = np.dot(temp[i], product_matrix[:, j]) + lambdaa * user_matrix[i][j]

    weight_average_matrix = weight_average_para * weight_average_matrix + (1 - weight_average_para) * (
                user_dervatives ** 2)  # 计算加权平均
    user_dervatives = user_dervatives / (weight_average_matrix ** 0.5)  # 计算变换的偏导
    return user_dervatives, weight_average_matrix


# 对产品特征进行偏导
# 输入：当前的用户矩阵、产品矩阵、缺失的二维表、惩罚因子 lambdaa
# 输出：产品特征偏导矩阵
def get_product_derivatives(ori_data, user_matrix, product_matrix, weight_average_matrix, lambdaa=1,
                            weight_average_para=0):
    nan_index = np.isnan(ori_data)  # 记录二维表中缺失的索引
    ori_data[nan_index] = 0  # 把缺失值填充为 0
    predict_data = np.dot(user_matrix, product_matrix.T)  # 计算预测的评分
    temp = predict_data - ori_data  # 计算两矩阵的差值
    temp[nan_index] = 0  # 缺失值不算在代价里
    ori_data[nan_index] = np.nan  # 恢复原数据

    num_product = product_matrix.shape[0]  # 计算产品数目
    feature_product = product_matrix.shape[1]  # 计算特征数目
    product_dervatives = np.random.rand(num_product, feature_product)  # 声明产品特征偏导数矩阵

    for i in range(num_product):
        for j in range(feature_product):
            product_dervatives[i][j] = np.dot(temp[:, i], user_matrix[:, j]) + lambdaa * product_matrix[i][j]

    weight_average_matrix = weight_average_para * weight_average_matrix + (1 - weight_average_para) * (
                product_dervatives ** 2)  # 计算加权平均
    product_dervatives = product_dervatives / (weight_average_matrix ** 0.5)  # 计算变换的偏导

    return product_dervatives, weight_average_matrix


# 根据含有缺失值的二维表，学习相关参数
# 输入：含有缺失值的二维表、用户特征初始矩阵、产品特征初始矩阵、迭代次数、学习效率 learning_rate、惩罚因子 lambdaa
# 输出：最优用户特征矩阵、最优产品特征矩阵
def CF(ori_data, user_matrix, product_matrix, iterate_num=500, learning_rate=0.01, lambdaa=1, weight_average_para=0.5):
    user_weight_average_matrix = np.zeros(user_matrix.shape)  # 初始化用户偏导加权平均为 0
    product_weight_average_matrix = np.zeros(product_matrix.shape)  # 初始化产品偏导加权平均为 0
    for i in range(iterate_num):
        cost = get_cost(ori_data, user_matrix, product_matrix, lambdaa)  # 计算当前代价
        user_derivatives, user_weight_average_matrix = get_user_derivatives(ori_data, user_matrix, product_matrix,
                                                                            user_weight_average_matrix, lambdaa,
                                                                            weight_average_para)  # 对用户特征求偏导
        product_derivates, product_weight_average_matrix = get_product_derivatives(ori_data, user_matrix,
                                                                                   product_matrix,
                                                                                   product_weight_average_matrix,
                                                                                   lambdaa,
                                                                                   weight_average_para)  # 对产品特征求偏导
        user_matrix = user_matrix - learning_rate * user_derivatives  # 更新参数
        product_matrix = product_matrix - learning_rate * product_derivates
        print i, 'th cost:', cost

    return user_matrix, product_matrix


# 根据学习的参数，进行评估
# 输入：用户特征矩阵、产品特征矩阵
# 输出：不含缺失值的二维表
def Evaluate_Score(user_matrix, product_matrix):
    return np.dot(user_matrix, product_matrix.T)


# 主函数
if __name__ == '__main__':
    ori_data = pd.read_csv('cf_data.csv')
    columns = ori_data.columns
    ori_data = np.array(ori_data)
    # ori_data = np.array([[5,5,np.nan,0,0],[5,np.nan,4,0,0],[0,np.nan,0,5,5],[0,0,np.nan,4,np.nan]])

    user_matrix, product_matrix = Initialize_Parameters(20, ori_data.shape[0], ori_data.shape[1])
    user_matrix, product_matrix = CF(ori_data, user_matrix, product_matrix, iterate_num=100, learning_rate=0.01,
                                     lambdaa=0)
    score = Evaluate_Score(user_matrix, product_matrix)
    predict_cf_data = pd.DataFrame(score, columns=columns)
    predict_cf_data.to_csv('predict_cf_data.csv', index=False)