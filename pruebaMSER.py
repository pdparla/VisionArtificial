import numpy as np
import cv2 as cv
import sys,os,math

#ZONA DEFINICIÓN DE CONSTANTES
MAX_DIVISION = 1.15
MASCARA_TRIANGULARES = np.array([[[ 4, 4, 6],[ 4, 5, 7],[ 5, 6, 7],[ 7, 7, 9],[ 6, 6, 8],[ 6, 7, 8],[ 5, 6, 7],[ 4, 4, 5],[ 5, 5, 6],[ 8, 8,10],[ 9,10,12],[10,11,14],[10,11,14],[ 9, 9,12],[ 7, 7,10],[ 6, 6, 8],[ 8, 8,11],[ 7, 7, 9],[ 7, 7, 8],[ 8, 9,10],[ 8, 8,10],[ 7, 8, 9],[ 9, 9,11],[ 7, 7, 9],[ 6, 6, 8]], [[ 4, 5, 6],[ 6, 7, 8],[ 7, 7, 9],[ 6, 7, 8],[ 6, 6, 7],[ 5, 5, 7],[ 4, 5, 5],[ 4, 5, 6],[ 5, 5, 7],[ 7, 7, 9],[11,11,13],[16,17,21],[20,21,26],[19,20,25],[12,12,16],[ 7, 7, 9],[ 8, 9,11],[ 7, 8,10],[ 5, 6, 7],[ 7, 7, 9],[ 7, 7, 9],[ 8, 8,10],[ 8, 8,10],[ 6, 7, 8],[ 6, 7, 8]], [[ 4, 5, 5],[ 7, 7, 9],[ 7, 7, 9],[ 6, 6, 8],[ 6, 7, 7],[ 7, 7, 9],[ 5, 5, 6],[ 4, 4, 5],[ 5, 6, 7],[10,11,13],[18,19,27],[29,31,45],[36,37,52],[34,36,48],[21,22,28],[10,10,12],[ 5, 5, 7],[ 5, 5, 7],[ 5, 6, 7],[11,12,14],[ 7, 8,10],[10,10,13],[ 7, 7,10],[ 6, 7, 8],[ 6, 7, 9]], [[ 3, 3, 4],[ 5, 5, 7],[ 4, 4, 5],[ 5, 5, 6],[ 6, 6, 7],[ 7, 7, 8],[ 4, 4, 5],[ 6, 6, 8],[ 6, 6, 8],[12,13,17],[23,25,38],[37,39,65],[42,45,76],[41,43,67],[35,37,49],[17,18,23],[ 6, 7, 9],[ 7, 7, 9],[10,10,12],[11,11,14],[ 7, 8,10],[ 7, 7, 9],[ 7, 8,11],[ 6, 6, 7],[ 8, 8,10]], [[ 2, 3, 3],[ 3, 3, 4],[ 4, 4, 5],[ 4, 4, 4],[ 6, 6, 7],[ 5, 5, 6],[ 5, 6, 7],[ 5, 6, 7],[ 4, 5, 6],[16,17,24],[32,33,53],[39,42,78],[43,47,91],[46,48,86],[44,45,66],[26,28,36],[11,12,15],[ 9, 9,12],[ 9, 9,12],[ 8, 8,10],[ 6, 6, 8],[ 9, 9,11],[ 7, 7, 9],[ 7, 7, 8],[ 4, 5, 6]], [[ 3, 4, 5],[ 4, 4, 6],[ 6, 6, 8],[ 4, 5, 6],[ 5, 5, 6],[ 6, 7, 8],[ 5, 5, 6],[ 5, 5, 7],[10,10,12],[21,22,34],[39,41,69],[44,47,86],[41,46,93],[43,46,92],[44,47,77],[37,38,53],[19,20,26],[10,10,13],[ 9, 9,11],[ 7, 7, 9],[ 7, 7, 9],[ 7, 7, 9],[ 6, 7, 8],[ 3, 3, 4],[ 4, 5, 6]], [[ 5, 5, 7],[ 5, 5, 6],[ 7, 7,10],[ 6, 6, 8],[ 5, 5, 6],[ 6, 6, 7],[ 5, 5, 7],[ 3, 3, 4],[14,15,20],[31,33,52],[41,44,77],[43,47,83],[51,55,93],[45,50,93],[46,49,88],[49,52,77],[30,32,43],[12,13,17],[ 7, 7, 9],[ 6, 6, 8],[ 4, 4, 5],[ 7, 7, 9],[ 6, 6, 8],[ 4, 4, 5],[ 5, 5, 6]], [[ 4, 4, 6],[ 4, 5, 5],[ 7, 8,10],[ 5, 5, 6],[ 5, 5, 6],[ 6, 6, 7],[ 4, 4, 5],[ 6, 7, 8],[22,23,34],[37,39,66],[40,43,78],[37,39,65],[40,41,59],[51,54,85],[44,48,89],[48,50,83],[40,41,58],[19,20,26],[ 6, 6, 7],[ 6, 6, 7],[ 8, 8,10],[ 5, 6, 7],[ 7, 7, 8],[ 6, 6, 7],[ 8, 8, 9]], [[ 4, 4, 5],[ 5, 5, 6],[ 4, 4, 5],[ 4, 5, 6],[ 4, 4, 6],[ 5, 5, 6],[ 8, 8,10],[12,14,18],[29,31,49],[41,44,77],[40,43,77],[31,32,49],[21,22,28],[41,43,57],[45,49,83],[42,45,85],[43,45,69],[31,32,43],[11,11,14],[ 7, 8,10],[ 8, 8,10],[ 7, 8, 9],[ 6, 6, 7],[ 6, 6, 7],[ 7, 7, 8]], [[ 5, 6, 7],[ 7, 7, 9],[ 6, 6, 7],[ 5, 5, 6],[ 4, 4, 5],[ 6, 6, 8],[ 8, 8,10],[22,23,32],[41,43,71],[41,44,81],[37,40,68],[25,26,35],[15,15,18],[20,21,25],[45,48,70],[42,46,87],[45,48,83],[41,43,60],[22,23,30],[12,12,15],[ 8, 9,11],[ 9, 9,12],[ 8, 8,10],[ 7, 7, 9],[ 6, 6, 8]], [[ 5, 6, 7],[ 7, 7, 9],[ 4, 4, 5],[ 3, 3, 4],[ 4, 5, 6],[ 5, 5, 7],[14,14,18],[31,34,51],[41,44,78],[38,40,75],[33,35,53],[17,18,23],[12,12,15],[11,12,14],[29,30,38],[46,51,84],[39,43,85],[45,47,74],[34,35,46],[13,13,16],[11,12,15],[ 8, 9,11],[ 7, 7, 9],[ 6, 6, 7],[ 7, 7, 9]], [[ 5, 5, 6],[ 5, 5, 6],[ 5, 5, 6],[ 3, 3, 4],[ 5, 6, 7],[ 6, 6, 7],[17,18,23],[39,42,68],[39,42,81],[38,40,69],[23,24,32],[15,16,20],[10,10,14],[ 8, 9,12],[11,12,15],[44,47,65],[39,44,84],[43,46,86],[47,49,70],[20,21,28],[13,14,17],[ 8, 9,11],[ 7, 8,10],[ 5, 5, 7],[ 6, 7, 9]], [[ 5, 5, 7],[ 5, 5, 6],[ 6, 6, 7],[ 5, 6, 7],[ 5, 5, 7],[10,10,12],[34,37,52],[42,45,81],[37,40,75],[34,35,53],[19,20,25],[14,15,18],[ 8, 9,11],[ 6, 7, 9],[ 7, 7, 9],[26,27,33],[45,49,77],[37,42,85],[46,48,79],[41,43,56],[15,16,20],[ 9, 9,12],[ 9,10,12],[ 7, 7, 9],[ 6, 6, 8]], [[ 6, 7, 8],[ 5, 6, 7],[ 6, 6, 7],[ 4, 5, 6],[ 6, 6, 8],[19,20,26],[39,41,66],[37,41,80],[40,42,71],[29,30,40],[15,15,18],[ 8, 8,10],[ 5, 5, 6],[ 4, 5, 6],[ 5, 6, 7],[12,12,14],[39,40,52],[41,45,83],[40,43,85],[48,50,71],[26,28,36],[10,11,13],[ 8, 9,11],[ 5, 5, 6],[ 6, 6, 8]], [[ 6, 7, 8],[ 6, 6, 8],[ 6, 6, 8],[ 5, 5, 6],[ 8, 9,11],[34,35,49],[40,43,79],[40,42,80],[36,37,54],[21,21,26],[13,13,16],[ 6, 6, 7],[ 5, 5, 6],[ 5, 5, 7],[ 5, 5, 6],[ 9, 9,11],[20,20,24],[46,49,73],[38,42,87],[52,55,91],[40,41,56],[18,19,24],[ 7, 8,10],[ 6, 7, 9],[ 6, 6, 8]], [[ 6, 7, 9],[ 4, 4, 5],[ 4, 4, 6],[ 2, 2, 3],[16,17,22],[40,43,68],[39,43,85],[37,39,67],[27,28,37],[17,18,21],[ 9,10,11],[ 5, 5, 6],[ 4, 4, 5],[ 5, 5, 6],[ 4, 4, 5],[ 4, 5, 5],[ 8, 9,10],[37,38,47],[44,48,84],[39,43,88],[48,49,73],[26,27,35],[11,11,15],[ 7, 8,10],[ 6, 7, 8]], [[ 7, 8,10],[ 6, 6, 8],[ 5, 5, 7],[10,11,13],[32,34,46],[42,46,82],[43,46,87],[39,40,58],[19,19,24],[13,14,16],[12,12,14],[ 7, 8, 9],[ 6, 6, 7],[ 5, 5, 6],[ 4, 4, 5],[ 5, 5, 6],[ 5, 5, 6],[15,15,18],[49,51,72],[39,44,88],[45,48,85],[44,46,62],[15,16,21],[10,10,13],[ 5, 5, 7]], [[ 6, 6, 8],[ 4, 4, 6],[ 6, 6, 7],[18,19,23],[42,45,69],[40,44,86],[43,46,77],[27,28,37],[13,14,17],[11,11,13],[14,14,16],[ 7, 7, 8],[ 3, 3, 4],[ 5, 5, 6],[ 6, 6, 7],[ 7, 7, 8],[ 3, 4, 4],[ 6, 7, 8],[29,30,37],[46,49,81],[39,43,87],[48,49,75],[27,28,36],[12,13,16],[ 5, 5, 7]], [[ 5, 5, 7],[ 5, 5, 7],[10,10,12],[31,32,42],[44,48,85],[43,46,87],[36,37,55],[22,22,27],[10,11,13],[ 8, 8,10],[ 7, 7, 8],[ 8, 8, 9],[ 4, 4, 5],[ 4, 4, 4],[ 6, 6, 7],[ 3, 3, 4],[ 1, 1, 1],[ 4, 4, 4],[13,13,15],[47,49,66],[40,44,84],[41,44,82],[45,46,63],[19,20,25],[ 9,10,12]], [[ 2, 3, 3],[ 5, 5, 7],[17,17,21],[39,41,63],[42,46,88],[43,46,77],[25,26,36],[15,16,19],[ 6, 6, 7],[ 6, 6, 7],[ 5, 5, 6],[ 8, 8,10],[ 4, 4, 5],[ 7, 7, 9],[ 5, 5, 6],[ 5, 5, 6],[ 4, 4, 5],[ 4, 4, 5],[ 9, 9,11],[33,34,40],[49,52,81],[39,42,86],[47,48,76],[34,35,46],[13,14,17]], [[ 4, 5, 6],[ 7, 7, 8],[31,33,42],[44,48,84],[44,48,91],[41,42,64],[20,20,27],[11,12,14],[ 7, 8, 9],[ 9, 9,11],[ 8, 8,10],[ 9, 9,10],[ 9,10,11],[ 9, 9,11],[12,13,15],[12,13,15],[13,13,16],[13,14,18],[15,16,22],[24,25,33],[51,53,75],[39,43,86],[43,46,87],[42,44,64],[20,20,26]], [[ 4, 5, 6],[14,14,18],[40,43,65],[42,46,91],[44,46,88],[43,43,66],[33,33,47],[35,35,47],[32,32,44],[35,36,48],[34,35,48],[32,33,47],[35,36,52],[34,36,52],[38,39,58],[36,37,57],[34,35,56],[34,35,57],[35,36,59],[39,40,64],[47,49,79],[38,41,85],[36,39,85],[48,50,78],[31,33,43]], [[ 7, 7, 9],[22,23,29],[39,42,73],[37,42,89],[39,42,93],[42,44,91],[40,42,85],[40,42,85],[37,39,82],[35,37,80],[34,35,79],[35,37,80],[33,35,77],[33,34,77],[35,37,80],[35,36,79],[35,37,79],[37,38,79],[37,39,79],[38,40,80],[40,42,84],[35,37,81],[34,37,81],[42,45,77],[35,36,47]], [[10,10,13],[29,30,42],[36,40,70],[35,39,80],[36,40,85],[37,40,85],[38,40,84],[36,38,81],[36,38,79],[36,37,77],[34,35,74],[36,37,75],[34,35,71],[36,37,72],[35,36,70],[36,37,69],[36,37,69],[36,38,69],[39,41,73],[37,38,69],[38,39,70],[36,37,66],[37,39,68],[34,36,59],[30,32,42]], [[ 7, 7, 8],[19,20,25],[28,30,42],[35,37,53],[36,37,54],[37,38,55],[35,37,53],[37,38,54],[33,34,49],[33,33,48],[33,35,50],[34,35,50],[32,33,49],[33,34,50],[29,30,43],[28,29,41],[29,30,43],[26,28,39],[28,29,41],[28,29,41],[29,30,42],[30,31,43],[28,30,42],[27,28,38],[19,19,24]]],dtype=np.uint8)
MASCARA_CIRCULARES = np.array([[[7,  8, 10],[6,  6,  9],[6,  7, 10],[7,  8, 11],[8,  8, 11],[8,  8, 11],[6,  6,  9],[7,  7, 10],[7,  7, 11],[8,  9, 13],[10, 10, 15],[13, 13, 18],[14, 14, 19],[15, 15, 21],[13, 13, 18],[10, 10, 15],[9,  9, 13],[8,  8, 11],[7,  8, 10],[7,  7, 10],[5,  6,  8],[7,  7, 10],[6,  7,  9],[6,  6,  8],[7,  8, 10]],[[7,  8, 11],[6,  6,  8],[6,  6,  8],[4,  5,  7],[6,  6,  8],[5,  5,  7],[6,  6,  8],[6,  6,  8],[11, 11, 14],[14, 14, 20],[18, 19, 26],[26, 27, 36],[28, 29, 40],[30, 31, 42],[28, 29, 38],[24, 25, 32],[17, 17, 22],[12, 13, 17],[9,  9, 12],[6,  6,  9],[4,  5,  6],[6,  6,  7],[5,  5,  7],[7,  7,  9],[6,  6,  8]],[[5,  5,  7],[5,  5,  6],[4,  4,  5],[5,  5,  6],[4,  4,  5],[6,  7,  9],[10, 11, 14],[17, 18, 24],[25, 26, 37],[34, 35, 53],[37, 38, 62],[41, 42, 71],[40, 42, 72],[39, 40, 70],[39, 41, 70],[41, 43, 69],[40, 41, 61],[35, 36, 49],[25, 25, 33],[13, 14, 18],[8,  8, 11],[6,  7,  8],[5,  5,  7],[6,  7,  8],[6,  6,  8]],[[5,  6,  7],[4,  5,  6],[4,  4,  5],[4,  4,  5],[6,  6,  7],[13, 13, 17],[23, 24, 33],[34, 35, 54],[37, 39, 67],[39, 41, 77],[39, 41, 80],[40, 42, 84],[39, 40, 83],[39, 40, 83],[38, 39, 82],[39, 41, 82],[40, 42, 80],[43, 45, 77],[42, 43, 66],[37, 37, 50],[20, 20, 25],[10, 10, 13],[6,  6,  8],[5,  6,  7],[4,  4,  5]],[[4,  4,  6],[4,  5,  6],[4,  4,  6],[6,  6,  8],[14, 15, 19],[27, 28, 41],[37, 39, 63],[39, 42, 76],[39, 41, 81],[40, 42, 83],[40, 42, 79],[40, 41, 76],[39, 40, 72],[39, 40, 72],[40, 41, 75],[41, 42, 81],[37, 39, 82],[36, 38, 81],[39, 41, 80],[43, 44, 73],[38, 39, 55],[23, 23, 30],[10, 11, 14],[6,  6,  7],[4,  4,  5]],[[4,  4,  6],[4,  5,  6],[5,  5,  6],[14, 14, 18],[27, 28, 40],[37, 40, 65],[41, 44, 81],[39, 43, 82],[39, 41, 75],[37, 39, 65],[36, 37, 57],[33, 34, 49],[30, 31, 44],[30, 30, 42],[33, 33, 47],[38, 39, 56],[42, 44, 69],[41, 43, 77],[35, 38, 79],[37, 40, 81],[41, 43, 73],[40, 41, 57],[23, 24, 31],[8,  9, 11],[5,  5,  7]],[[4,  4,  6],[5,  5,  7],[11, 12, 14],[25, 26, 36],[38, 40, 64],[39, 42, 78],[39, 43, 80],[39, 41, 70],[35, 36, 55],[30, 31, 43],[23, 24, 32],[17, 18, 23],[13, 14, 18],[11, 11, 15],[14, 14, 18],[17, 17, 23],[26, 26, 34],[39, 40, 55],[41, 45, 71],[36, 40, 79],[36, 40, 80],[41, 43, 72],[41, 42, 56],[17, 18, 23],[7,  7,  9]],[[4,  5,  6],[7,  7,  9],[18, 19, 24],[35, 36, 55],[40, 43, 76],[39, 42, 80],[38, 40, 70],[35, 37, 54],[26, 27, 37],[18, 18, 24],[10, 10, 13],[7,  7,  9],[5,  5,  6],[4,  4,  5],[5,  5,  6],[6,  6,  7],[11, 11, 13],[23, 24, 29],[36, 38, 49],[42, 45, 70],[34, 38, 78],[36, 38, 77],[42, 44, 68],[31, 32, 42],[11, 12, 15]],[[5,  5,  6],[10, 10, 13],[25, 26, 37],[39, 41, 69],[41, 43, 82],[39, 41, 74],[37, 39, 59],[32, 33, 44],[23, 23, 30],[16, 16, 20],[9,  9, 11],[5,  5,  6],[3,  3,  4],[3,  3,  3],[5,  5,  5],[4,  4,  5],[5,  5,  6],[10, 10, 12],[20, 21, 25],[36, 37, 50],[40, 43, 75],[33, 35, 77],[39, 41, 76],[42, 43, 59],[19, 21, 27]],[[5,  5,  7],[16, 16, 21],[34, 36, 54],[40, 42, 76],[42, 43, 82],[39, 40, 66],[35, 36, 50],[27, 28, 37],[20, 20, 26],[15, 15, 20],[11, 11, 15],[7,  7,  9],[5,  5,  6],[5,  5,  6],[5,  5,  6],[3,  3,  4],[4,  4,  5],[7,  7,  9],[10, 10, 12],[24, 24, 30],[40, 42, 61],[34, 37, 76],[33, 35, 74],[43, 44, 67],[27, 28, 38]],[[5,  6,  8],[20, 21, 28],[34, 36, 58],[40, 42, 79],[41, 41, 77],[35, 36, 55],[33, 34, 45],[23, 23, 31],[13, 14, 20],[12, 12, 18],[12, 12, 19],[8,  8, 13],[5,  6,  8],[8,  8, 10],[7,  7,  8],[5,  5,  6],[5,  5,  7],[8,  8, 10],[8,  8, 10],[14, 14, 17],[31, 32, 43],[38, 41, 74],[31, 32, 74],[40, 41, 70],[35, 36, 48]],[[10, 11, 14],[25, 26, 35],[36, 38, 65],[41, 42, 81],[41, 42, 74],[31, 32, 46],[25, 25, 33],[22, 22, 29],[12, 13, 19],[10, 10, 17],[11, 11, 18],[9,  9, 15],[6,  6,  9],[10, 10, 12],[7,  7,  9],[4,  4,  5],[3,  3,  4],[6,  6,  8],[8,  8, 10],[11, 11, 13],[25, 26, 32],[43, 45, 73],[31, 32, 74],[38, 38, 72],[38, 39, 53]],[[10, 10, 13],[27, 28, 39],[39, 41, 70],[43, 44, 84],[44, 44, 75],[31, 32, 45],[22, 23, 29],[20, 20, 26],[12, 12, 19],[9,  9, 16],[10, 10, 18],[10, 10, 17],[9,  9, 13],[11, 11, 14],[7,  7,  9],[5,  5,  6],[3,  3,  4],[7,  7,  8],[8,  8, 10],[9,  9, 11],[21, 22, 27],[43, 45, 69],[32, 33, 75],[36, 36, 71],[40, 41, 57]],[[8,  9, 12],[27, 28, 38],[39, 41, 70],[43, 44, 84],[43, 43, 74],[30, 31, 44],[21, 22, 28],[16, 16, 24],[12, 12, 20],[11, 11, 21],[11, 11, 21],[10, 10, 19],[9, 10, 15],[9, 10, 12],[6,  6,  9],[5,  5,  6],[4,  4,  5],[6,  6,  7],[8,  8, 10],[8,  8, 10],[19, 20, 24],[44, 46, 69],[33, 34, 76],[35, 36, 71],[40, 42, 58]],[[8,  8, 10],[26, 27, 35],[38, 40, 67],[43, 44, 84],[43, 43, 76],[32, 33, 46],[22, 22, 29],[16, 17, 23],[11, 11, 17],[11, 11, 17],[14, 15, 22],[13, 14, 21],[9,  9, 13],[9,  9, 12],[7,  7,  9],[5,  5,  7],[4,  4,  5],[6,  7,  8],[8,  8, 10],[9,  9, 11],[21, 21, 27],[42, 45, 71],[32, 33, 75],[36, 37, 72],[41, 43, 58]],[[7,  8, 10],[19, 20, 26],[35, 37, 60],[42, 44, 82],[42, 42, 78],[35, 36, 52],[27, 28, 35],[17, 17, 21],[11, 11, 14],[10, 10, 13],[12, 12, 15],[11, 12, 16],[8,  8, 11],[8,  8, 10],[9,  9, 11],[6,  6,  7],[5,  5,  6],[7,  8,  9],[8,  8, 10],[11, 11, 14],[27, 28, 36],[40, 43, 74],[31, 32, 74],[40, 41, 72],[36, 38, 50]],[[6,  6,  8],[16, 16, 21],[34, 35, 53],[42, 44, 79],[43, 44, 84],[41, 42, 65],[32, 32, 42],[20, 21, 25],[11, 12, 14],[9,  9, 11],[9,  9, 11],[7,  7, 10],[4,  5,  6],[6,  7,  8],[7,  7,  9],[6,  6,  7],[5,  5,  6],[7,  7,  9],[7,  7,  9],[18, 18, 22],[39, 41, 57],[36, 38, 75],[32, 33, 73],[45, 46, 72],[33, 34, 45]],[[4,  4,  5],[13, 13, 17],[30, 31, 43],[42, 44, 74],[42, 44, 85],[43, 44, 76],[35, 36, 50],[27, 28, 34],[16, 17, 20],[10, 11, 13],[7,  7,  8],[5,  5,  6],[3,  3,  4],[4,  4,  5],[7,  7,  8],[5,  5,  6],[6,  6,  7],[7,  7,  9],[13, 14, 16],[31, 32, 40],[43, 45, 73],[34, 36, 76],[35, 36, 72],[44, 45, 64],[24, 25, 33]],[[4,  5,  6],[9,  9, 11],[24, 25, 32],[40, 42, 64],[41, 44, 82],[40, 42, 83],[41, 42, 67],[34, 35, 46],[24, 24, 30],[11, 12, 14],[4,  4,  5],[3,  3,  3],[2,  2,  2],[1,  1,  1],[2,  2,  2],[3,  3,  4],[4,  4,  5],[12, 12, 14],[28, 29, 36],[43, 46, 67],[37, 40, 77],[33, 35, 76],[43, 44, 73],[35, 36, 49],[14, 15, 20]],[[5,  5,  7],[5,  5,  7],[16, 16, 20],[33, 34, 47],[43, 45, 74],[39, 42, 82],[39, 42, 81],[42, 44, 68],[33, 34, 45],[23, 24, 29],[11, 12, 14],[6,  6,  7],[3,  3,  4],[2,  2,  3],[3,  3,  3],[5,  5,  6],[12, 12, 14],[28, 30, 37],[39, 42, 61],[36, 39, 73],[32, 35, 76],[39, 41, 75],[41, 42, 60],[23, 24, 32],[8,  9, 11]],[[4,  4,  6],[5,  5,  6],[9,  9, 11],[22, 22, 28],[36, 37, 52],[40, 43, 74],[37, 40, 80],[38, 40, 81],[41, 43, 72],[39, 40, 57],[31, 32, 42],[24, 24, 31],[20, 20, 24],[15, 15, 18],[18, 18, 23],[28, 29, 37],[38, 40, 55],[41, 44, 71],[34, 37, 74],[32, 35, 75],[37, 39, 75],[44, 45, 67],[27, 28, 38],[13, 14, 17],[7,  7,  9]],[[4,  4,  5],[3,  3,  5],[5,  6,  7],[10, 10, 13],[24, 24, 31],[36, 37, 53],[41, 43, 74],[37, 40, 79],[35, 37, 79],[38, 40, 80],[40, 41, 75],[41, 42, 69],[39, 39, 61],[38, 38, 60],[41, 41, 66],[42, 43, 74],[37, 38, 75],[32, 34, 75],[32, 35, 75],[37, 39, 73],[42, 43, 65],[31, 32, 42],[14, 15, 19],[8,  8, 10],[7,  7,  9]],[[3,  4,  5],[4,  4,  5],[4,  4,  6],[5,  5,  6],[10, 11, 13],[20, 21, 26],[34, 35, 49],[40, 42, 67],[38, 41, 77],[36, 37, 79],[33, 34, 77],[34, 35, 78],[35, 35, 77],[35, 36, 78],[34, 35, 77],[32, 33, 75],[32, 33, 74],[34, 36, 73],[36, 38, 67],[39, 40, 58],[26, 27, 36],[15, 15, 20],[8,  9, 11],[5,  6,  7],[5,  5,  7]],[[3,  3,  4],[5,  5,  6],[4,  4,  5],[4,  5,  6],[5,  6,  7],[8,  8, 10],[17, 17, 21],[28, 29, 37],[38, 39, 56],[40, 42, 67],[38, 40, 71],[38, 39, 74],[38, 39, 76],[37, 39, 76],[36, 38, 73],[37, 39, 70],[41, 42, 69],[38, 39, 58],[32, 33, 45],[20, 21, 27],[12, 13, 16],[8,  9, 10],[7,  7,  9],[5,  6,  7],[4,  4,  6]],[[4,  4,  5],[5,  5,  7],[4,  4,  6],[5,  6,  7],[4,  5,  6],[6,  6,  7],[6,  6,  8],[10, 11, 13],[19, 19, 24],[23, 24, 30],[31, 32, 41],[34, 35, 48],[38, 39, 55],[37, 38, 54],[36, 37, 51],[34, 35, 47],[27, 27, 36],[19, 20, 26],[14, 15, 19],[9,  9, 12],[6,  6,  8],[6,  7,  8],[5,  5,  6],[5,  5,  6],[5,  5,  7]]],dtype=np.uint8)
MIN_DIVISION = 0.85
MASCARA_STOP = np.array([[[  9, 10, 12],[  7,  7, 10],[ 10, 10, 14],[  7,  7,  8],[  6,  6,  7],[  7,  7,  8],[  7,  8, 10],[  2,  2,  2],[  7,  7,  9],[  1,  1,  2],[  3,  3,  4],[  8,  9, 10],[ 16, 17, 19],[  4,  4,  5],[  9,  9, 11],[  5,  5,  6],[  6,  6,  7],[  7,  7,  9],[  3,  4,  4],[  0,  0,  0],[  0,  0,  0],[  0,  0,  0],[  0,  0,  0],[  0,  0,  0],[  0,  0,  0]], [[ 11, 11, 13],[  6,  5,  8],[  8,  8, 11],[  7,  7,  8],[  6,  6,  8],[  1,  1,  1],[  2,  2,  3],[  3,  3,  4],[ 17, 18, 20],[  6,  6,  7],[ 12, 12, 14],[ 16, 17, 21],[ 19, 20, 25],[ 21, 22, 26],[ 31, 30, 35],[ 23, 23, 27],[ 20, 20, 24],[ 12, 13, 15],[ 11, 11, 13],[  2,  2,  3],[  5,  5,  6],[  1,  1,  1],[  2,  2,  2],[  0,  0,  0],[  0,  0,  0]], [[  7,  7,  9],[  8,  8, 10],[  9, 10, 13],[ 10,  9, 12],[ 10, 10, 13],[  0,  0,  0],[  9,  9, 11],[ 36, 38, 51],[ 54, 54, 79],[ 60, 60, 93],[ 59, 58, 93],[ 63, 63,105],[ 59, 60,105],[ 57, 57,103],[ 62, 63,109],[ 54, 54, 98],[ 57, 58, 97],[ 60, 60, 78],[ 31, 32, 36],[  6,  7,  8],[  5,  5,  6],[  8,  8,  9],[  2,  3,  3],[  3,  3,  4],[  0,  0,  0]], [[ 10, 11, 15],[ 15, 15, 19],[  7,  7, 10],[  9,  8, 11],[ 10, 10, 12],[ 10, 11, 13],[ 37, 37, 51],[ 48, 50, 87],[ 48, 50, 98],[ 51, 52,105],[ 50, 51,105],[ 48, 49,105],[ 47, 48,105],[ 47, 48,105],[ 46, 47,106],[ 46, 48,105],[ 50, 52,108],[ 59, 61,110],[ 56, 56, 79],[ 36, 37, 43],[  6,  6,  8],[  4,  5,  6],[ 12, 12, 14],[ 10,  9, 12],[  3,  3,  3]], [[ 10,  9, 12],[  7,  7,  9],[  5,  5,  7],[ 21, 21, 25],[ 19, 19, 24],[ 40, 41, 55],[ 37, 37, 71],[ 47, 49, 96],[ 47, 49,105],[ 43, 43,102],[ 39, 40,100],[ 40, 41,102],[ 42, 44,105],[ 42, 42,104],[ 41, 42,104],[ 41, 41,103],[ 41, 42,104],[ 43, 45,103],[ 54, 56,108],[ 59, 60, 87],[ 35, 35, 44],[ 11, 12, 14],[  9,  9, 12],[  1,  1,  2],[  2,  2,  3]], [[  8,  9, 11],[  5,  5,  7],[  4,  3,  5],[  5,  5,  6],[ 35, 35, 48],[ 46, 47, 81],[ 38, 38, 82],[ 43, 45, 99],[ 42, 43,102],[ 41, 41,103],[ 38, 39,101],[ 36, 37, 99],[ 36, 37,100],[ 37, 38,101],[ 37, 37,100],[ 35, 36,100],[ 37, 38,101],[ 35, 37, 99],[ 38, 41,101],[ 47, 49,102],[ 56, 57, 89],[ 35, 35, 45],[ 14, 14, 18],[ 12, 12, 14],[  3,  3,  4]], [[  4,  4,  6],[  5,  5,  7],[  7,  7,  9],[ 23, 23, 32],[ 44, 46, 78],[ 52, 53,101],[ 40, 42, 96],[ 40, 41,100],[ 40, 40,102],[ 38, 39,101],[ 36, 36, 99],[ 35, 36, 99],[ 34, 35, 97],[ 34, 34, 95],[ 35, 35, 94],[ 37, 38,102],[ 33, 34, 95],[ 32, 33, 93],[ 33, 34, 96],[ 35, 36, 95],[ 45, 48,101],[ 65, 65,102],[ 40, 40, 51],[ 19, 19, 23],[ 19, 20, 22]], [[  6,  6,  7],[  6,  6,  8],[ 24, 25, 33],[ 55, 57, 87],[ 49, 49, 96],[ 44, 46,100],[ 36, 37, 93],[ 37, 38, 98],[ 36, 36, 97],[ 36, 36, 97],[ 36, 36, 98],[ 36, 36, 98],[ 35, 35, 94],[ 33, 33, 92],[ 33, 33, 93],[ 33, 33, 93],[ 32, 33, 92],[ 32, 32, 94],[ 32, 33, 93],[ 35, 36, 94],[ 33, 35, 91],[ 41, 42, 92],[ 54, 55, 91],[ 45, 46, 57],[ 20, 20, 23]], [[  5,  5,  6],[ 27, 26, 33],[ 41, 43, 69],[ 49, 50, 95],[ 43, 45, 95],[ 44, 45, 97],[ 40, 41, 96],[ 38, 39, 95],[ 41, 42, 96],[ 43, 44, 93],[ 46, 47, 97],[ 50, 51,103],[ 40, 41, 97],[ 41, 43, 95],[ 46, 48, 90],[ 44, 45, 91],[ 38, 38, 97],[ 46, 45, 97],[ 30, 31, 63],[ 35, 38, 67],[ 52, 55, 90],[ 42, 45, 95],[ 40, 41, 91],[ 54, 56, 80],[ 13, 13, 16]], [[  4,  4,  6],[ 50, 50, 64],[ 57, 57, 97],[ 54, 56,104],[ 49, 52, 87],[ 51, 53, 80],[ 69, 72,110],[ 64, 64,112],[ 45, 45, 73],[ 41, 41, 59],[ 32, 32, 45],[ 52, 53, 79],[ 66, 66,112],[ 38, 39, 63],[ 48, 48, 67],[ 53, 54, 73],[ 62, 64,106],[ 57, 55,100],[ 51, 52, 74],[ 49, 50, 72],[ 65, 67, 85],[ 61, 65, 95],[ 48, 49, 99],[ 43, 45, 71],[  7,  7, 10]],[[  3,  3,  5],[ 41, 40, 51],[ 60, 59,102],[ 50, 49, 86],[ 46, 48, 70],[ 54, 55, 80],[ 65, 65, 83],[ 90, 90,135],[ 77, 76,119],[ 42, 44, 59],[ 50, 53, 71],[ 57, 60, 97],[ 63, 62, 96],[ 62, 63, 82],[ 70, 71,107],[ 66, 67, 85],[ 75, 76,104],[ 69, 67,112],[ 55, 56, 76],[ 52, 52, 81],[ 71, 73, 93],[ 55, 59, 78],[ 52, 50, 95],[ 45, 46, 74],[ 16, 17, 24]], [[  3,  3,  5],[ 41, 40, 48],[ 64, 64,107],[ 49, 50, 82],[ 60, 63, 82],[ 62, 63,101],[ 56, 56, 83],[ 75, 75,125],[ 60, 61,114],[ 59, 60, 85],[ 59, 61, 76],[ 47, 47, 88],[ 62, 61, 98],[ 62, 64, 82],[ 73, 75,113],[ 48, 48, 67],[ 55, 56, 76],[ 58, 57, 96],[ 58, 59, 78],[ 57, 59, 83],[ 49, 51, 67],[ 49, 52, 69],[ 53, 51, 95],[ 40, 41, 70],[ 24, 25, 33]], [[  3,  3,  4],[ 24, 24, 28],[ 56, 57, 98],[ 55, 53, 93],[ 54, 55, 72],[ 69, 73, 99],[ 71, 74,118],[ 59, 61,114],[ 55, 55,111],[ 53, 54, 84],[ 58, 60, 75],[ 52, 52, 96],[ 61, 59,101],[ 55, 56, 73],[ 62, 63, 99],[ 56, 57, 80],[ 57, 59, 78],[ 58, 57, 96],[ 46, 47, 63],[ 51, 53, 65],[ 37, 40, 51],[ 60, 62, 96],[ 48, 46, 93],[ 57, 57, 91],[ 23, 24, 33]], [[  3,  3,  4],[ 24, 24, 28],[ 52, 53, 92],[ 41, 41, 94],[ 36, 35, 66],[ 49, 50, 63],[ 60, 61, 75],[ 57, 60, 97],[ 47, 48,102],[ 53, 53, 86],[ 55, 58, 73],[ 45, 47, 89],[ 49, 47, 91],[ 49, 49, 66],[ 58, 59, 92],[ 62, 62, 88],[ 50, 53, 70],[ 59, 59, 99],[ 38, 38, 53],[ 48, 51, 71],[ 50, 52, 86],[ 50, 51, 95],[ 44, 43, 94],[ 51, 52, 87],[ 23, 23, 33]], [[  6,  6,  8],[ 22, 23, 27],[ 46, 47, 83],[ 44, 44, 99],[ 49, 50,106],[ 59, 61,108],[ 46, 47, 60],[ 73, 76,103],[ 60, 60,114],[ 48, 48, 82],[ 42, 44, 55],[ 49, 51, 93],[ 47, 46, 91],[ 54, 55, 74],[ 46, 48, 76],[ 59, 61, 87],[ 46, 48, 63],[ 58, 58, 97],[ 63, 63, 83],[ 52, 55, 81],[ 43, 44, 88],[ 41, 41, 93],[ 40, 39, 92],[ 50, 49, 87],[ 26, 26, 36]], [[  7,  7,  9],[ 23, 24, 27],[ 48, 48, 83],[ 49, 49, 93],[ 48, 49, 76],[ 59, 61,106],[ 44, 45, 60],[ 71, 74, 98],[ 62, 64,116],[ 54, 54, 91],[ 62, 64, 81],[ 55, 58,100],[ 46, 45, 94],[ 58, 57, 78],[ 69, 71, 87],[ 46, 49, 63],[ 75, 78,100],[ 52, 51, 92],[ 80, 80,108],[ 74, 77,107],[ 39, 40, 88],[ 42, 41, 97],[ 41, 40, 95],[ 50, 50, 90],[ 35, 35, 46]], [[  6,  6,  8],[ 19, 19, 22],[ 63, 65,101],[ 48, 47, 94],[ 51, 50, 72],[ 36, 37, 50],[ 39, 41, 52],[ 68, 70,103],[ 59, 59,113],[ 63, 62,110],[ 62, 63, 87],[ 58, 60,103],[ 40, 40, 93],[ 67, 65,104],[ 59, 59, 75],[ 71, 72, 93],[ 72, 75,115],[ 53, 52,102],[ 77, 76,118],[ 81, 82,126],[ 45, 45, 99],[ 42, 43, 99],[ 41, 42, 96],[ 48, 51, 87],[ 31, 32, 41]], [[  4,  4,  6],[ 20, 20, 23],[ 55, 56, 86],[ 44, 45, 97],[ 60, 60,110],[ 73, 73,111],[ 70, 71,110],[ 63, 66,119],[ 50, 52,111],[ 49, 49,111],[ 67, 67,125],[ 54, 55,109],[ 35, 35, 91],[ 44, 45,103],[ 56, 55,108],[ 64, 63,117],[ 52, 52,107],[ 42, 42, 99],[ 49, 49,108],[ 55, 56,114],[ 41, 41, 98],[ 42, 43,100],[ 43, 46, 91],[ 38, 39, 61],[ 32, 33, 41]], [[  4,  4,  6],[ 19, 20, 23],[ 54, 56, 68],[ 50, 53, 95],[ 45, 48,103],[ 57, 58,120],[ 57, 58,120],[ 51, 53,116],[ 46, 48,114],[ 42, 44,110],[ 46, 47,112],[ 41, 42,102],[ 32, 33, 92],[ 31, 31, 90],[ 45, 44,106],[ 45, 45,104],[ 43, 43,103],[ 40, 40,102],[ 38, 38, 99],[ 42, 43,103],[ 42, 42, 99],[ 49, 49, 98],[ 34, 36, 61],[ 32, 31, 43],[ 13, 13, 18]], [[  9,  9, 12],[  7,  8,  9],[ 25, 25, 29],[ 54, 55, 70],[ 56, 60,102],[ 50, 53,109],[ 47, 47,109],[ 45, 46,111],[ 42, 44,111],[ 42, 43,111],[ 45, 46,113],[ 38, 39,101],[ 32, 33, 92],[ 35, 35, 94],[ 39, 39,100],[ 43, 43,103],[ 41, 41,101],[ 40, 40,100],[ 35, 36, 95],[ 41, 41,100],[ 45, 46, 96],[ 46, 48, 78],[ 34, 34, 47],[ 17, 17, 24],[  6,  6,  9]], [[  8,  8, 10],[  4,  4,  5],[  2,  2,  4],[ 26, 26, 32],[ 58, 59, 72],[ 63, 66,106],[ 49, 51,108],[ 41, 42,105],[ 45, 47,114],[ 43, 44,112],[ 43, 44,111],[ 41, 41,107],[ 40, 40,103],[ 39, 40,102],[ 38, 38,100],[ 40, 40,101],[ 39, 39,100],[ 37, 36, 95],[ 34, 34, 91],[ 39, 41, 93],[ 47, 50, 81],[ 35, 36, 51],[ 17, 17, 24],[ 10, 10, 15],[ 13, 13, 17]], [[  5,  5,  7],[  4,  4,  5],[  2,  2,  3],[ 16, 16, 20],[ 31, 32, 38],[ 41, 42, 51],[ 61, 64,101],[ 47, 50,106],[ 41, 43,107],[ 47, 48,114],[ 41, 42,108],[ 41, 42,107],[ 41, 41,104],[ 40, 40,101],[ 38, 39, 99],[ 39, 39,101],[ 38, 39, 99],[ 39, 40, 99],[ 37, 39, 93],[ 56, 58, 94],[ 51, 52, 70],[ 22, 23, 31],[ 10, 10, 14],[  5,  5,  8],[  6,  6,  7]], [[  7,  7, 12],[  4,  4,  5],[ 12, 13, 15],[ 15, 15, 18],[ 23, 23, 28],[ 18, 18, 22],[ 26, 27, 33],[ 63, 68,103],[ 47, 50,105],[ 42, 44,106],[ 46, 47,111],[ 43, 43,105],[ 39, 40, 99],[ 40, 41,100],[ 41, 42,101],[ 40, 41, 99],[ 38, 37, 93],[ 37, 39, 91],[ 45, 47, 83],[ 42, 43, 60],[ 24, 24, 32],[ 12, 13, 17],[  4,  5,  8],[  6,  6,  8],[ 15, 15, 17]], [[  6,  5,  9],[  7,  7, 10],[ 21, 20, 25],[  7,  8, 10],[  6,  6,  7],[  7,  7, 10],[ 20, 21, 25],[ 24, 25, 31],[ 67, 71,101],[ 55, 58,104],[ 53, 54,102],[ 52, 53,101],[ 58, 60,105],[ 60, 61,101],[ 56, 57, 92],[ 50, 52, 85],[ 39, 40, 69],[ 37, 39, 60],[ 37, 38, 53],[ 15, 16, 22],[ 14, 15, 20],[  6,  7, 10],[  5,  5,  7],[  0,  1,  1],[  0,  0,  0]], [[ 13, 13, 18],[ 16, 17, 21],[ 12, 12, 17],[ 11, 11, 13],[  5,  5,  6],[  9, 10, 13],[ 12, 12, 14],[ 12, 12, 16],[ 26, 27, 33],[ 37, 38, 47],[ 36, 37, 48],[ 41, 41, 52],[ 40, 42, 54],[ 35, 35, 45],[ 37, 38, 47],[ 24, 24, 33],[ 22, 22, 29],[ 18, 18, 24],[ 18, 19, 24],[ 14, 14, 19],[  6,  6,  9],[ 12, 12, 15],[ 15, 16, 17],[  0,  0,  0],[  0,  0,  0]]] , dtype=np.uint8)
UMBRAL_APARIENCIA = 0.3

def cogerImagen(name_img):
    try:
       img = cv.imread(name_img)
       return img
    except Exception:
        print('No se puede cargar la imagen,saliendo')
        sys.exit(-1)

def hazmeCuadrado(rectangulo):

    x = rectangulo[0]
    y = rectangulo[1]
    w = rectangulo[2]
    h = rectangulo[3]
    centroX = round(x + w/2)
    centroY = round(y + h/2)
    if w > h:
        w = int(round(w * 1.7))
        h = w
    else:
        h = int(round(h * 1.7))
        w = h
    x = int(round(centroX - w/2))
    if x < 0:
        x = 0
    y = int(round(centroY - h/2))
    if y < 0:
        x = 0
    return np.array([x,y,w,h])

#https://stackoverflow.com/questions/29481518/python-equivalent-of-matlab-corr2
def mean2(x):
    y = np.sum(x) / np.size(x);
    return y

def corr2(a,b):
    a = a - mean2(a)
    b = b - mean2(b)

    r = (a*b).sum() / math.sqrt((a*a).sum() * (b*b).sum());
    return r

# Mejor contraste en imagen: sacado de https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
def mejorContraste(img):
    #-----Converting image to LAB Color model-----------------------------------
    lab= cv.cvtColor(img, cv.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv.cvtColor(limg, cv.COLOR_LAB2BGR)
    return final

#https://stackoverflow.com/questions/32522989/opencv-better-detection-of-red-color/32523532?noredirect=1#comment74897695_32523532
def generarMascaraRojos(img):
    inversa = ~img
    hsv_inversa = cv.cvtColor(inversa, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv_inversa, np.array([90 - 10, 10, 70]), np.array([90 + 10, 255, 255]))
    return mask

def comprobarMascara(mascara, mascara_cte):
    coef = corr2(mascara, mascara_cte)
    return coef

if __name__ == '__main__':

    # Mascaras: circular,triangular,octogonal
    m_c, m_t, m_o = np.zeros(shape=(25, 25, 3),dtype=np.uint8), np.zeros(shape=(25, 25, 3),dtype=np.uint8), np.zeros(shape=(25, 25, 3),dtype=np.uint8)
    for imagen in os.listdir('./train_10_ejemplos/'):
        img = cogerImagen(f'./train_10_ejemplos/{imagen}')
        imgcontraste = mejorContraste(img)
        mser = cv.MSER_create(_delta = 7, _max_area =20000,_max_variation = .15)
        gray = cv.cvtColor(imgcontraste, cv.COLOR_BGR2GRAY)
        _ , x  = mser.detectRegions(gray)
        for rectangle in x:
            # Por cada rectangulo, miramos el alto y el ancho y a partir de ahi, filtramos
            if (rectangle[2]/rectangle[3] >= MIN_DIVISION) and (rectangle[2]/rectangle[3] <= MAX_DIVISION):
                x,y,w,h = hazmeCuadrado(rectangle)
                rectanguloGris = gray[y:y+h,x:x+w]
                rectanguloColor = imgcontraste[y:y + h, x:x + w]
                mask = generarMascaraRojos(rectanguloColor)
                #Aplicamos la mascara a la imagen
                res = cv.resize(cv.bitwise_and(rectanguloColor, rectanguloColor, mask=mask),(25,25))
                porcentaje_warning = comprobarMascara(res,MASCARA_TRIANGULARES)
                porcentaje_obligacion = comprobarMascara(res, MASCARA_CIRCULARES)
                porcentaje_stop = comprobarMascara(res, MASCARA_STOP)
                maximo = max(porcentaje_warning,porcentaje_obligacion,porcentaje_stop)
                if maximo == porcentaje_warning and maximo > UMBRAL_APARIENCIA:
                    print('Detectada warning')
                elif maximo == porcentaje_obligacion and maximo > UMBRAL_APARIENCIA:
                    print('Detectada obligacion')
                elif maximo == porcentaje_stop and maximo > UMBRAL_APARIENCIA:
                    print('Detectada señal de stop')
                else:
                    print('No es señal')
                # resFinal = cv.resize(res, (300,300))
                # imgOriginal = cv.resize(rectanguloColor, (300,300))
                # imgGris = cv.resize(rectanguloGris, (300, 300))
                #
                # cv.imshow('Imagen mascara', resFinal)
                # cv.imshow('Imagen original', imgOriginal)
                # cv.imshow('Imagen gris', imgGris)
                # k = cv.waitKey(0)
                # if k == ord('c'):
                #     m_c = cv.add(m_c,cv.resize(res,(25,25)))
                #     break
                # elif k == ord('t'):
                #     m_c = cv.add(m_c,cv.resize(res,(25,25)))
                #     break
                # elif k == ord('o'):
                #     m_c = cv.add(m_c,cv.resize(res,(25,25)))
                #     break
                # elif k == ord('s'):
                #     continue
                # elif k == 27:
                #     break
cv.destroyAllWindows()
