from shapely import wkt
import netCDF4
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import urllib



wcs_base_url = '''https://vortices.npm.ac.uk/thredds/wcs/CCI_ALL-v1.0-MONTHLY?crs=OGC:CRS84&service=WCS&format=NetCDF3&request=GetCoverage&version=1.0.0&bbox=%s,%s,%s,%s&coverage=chlor_a&time=2007-07-01/2007-08-01'''

trim_sizes = {
   "polygon" : slice(9,-2),
   "line" : slice(11,-2)
}

def create_wcs_url(bounds):
   return wcs_base_url % (bounds[0],bounds[1],bounds[2],bounds[3])


def find_closest(arr, val):
   """
  Finds the position in the array where the array value matches
  the value specified by the user
  """
   current_closest = 120310231023
   current_idx = None
   for i in range(len(arr)):
      if abs(arr[i]-val)<current_closest:
         current_closest = abs(arr[i]-val)
         current_idx=i
   return current_idx


def create_mask(poly, variable, poly_type="polygon"):
   '''
   takes a Well Known Text polygon or line 
   and produces a masking array for use with numpy
   @param poly - WKT polygon or line
   @param variable - WCS variable to mask off
   @param type - one from [polygon, line]
   '''
   loaded_poly = wkt.loads(poly)
   wcs_envelope = loaded_poly.envelope
   bounds =  wcs_envelope.bounds
   wcs_url = wcs_base_url % (bounds[0],bounds[1],bounds[2],bounds[3])
   testfile=urllib.URLopener()
   testfile.retrieve(wcs_url,"%s.nc" % variable)
   to_be_masked = netCDF4.Dataset('./%s.nc'  % variable, 'r')

   chl = to_be_masked.variables[variable][:]

   latvals = to_be_masked.variables['lat'][:]
   lonvals = to_be_masked.variables['lon'][:]

   poly = poly[trim_sizes[poly_type]]
   print poly
   poly = poly.split(',')
   poly = [x.split() for x in poly]

   found_lats = [find_closest(latvals, float(x[1])) for x in poly]
   found_lons = [find_closest(lonvals, float(x[0])) for x in poly]

   found = zip(found_lons,found_lats)
   img = Image.new('L', (chl.shape[2],chl.shape[1]), 0)

   if poly_type == 'polygon':
      ImageDraw.Draw(img).polygon(found,  outline=2, fill=2)
   if poly_type == 'line':
      ImageDraw.Draw(img).line(found,   fill=2)

   masker = np.array(img)
   masked_variable = np.ma.masked_array(chl[0,:], [x != 2 for x in masker])
   return masked_variable


if __name__ == '__main__':
   wkt_poly = '''POLYGON((-29.35546875 60.369873046875, -33.57421875 56.678466796875, -34.1015625 55.096435546875, -30.76171875 52.108154296875, -27.94921875 48.416748046875, -28.125 45.428466796875, -29.1796875 41.385498046875, -31.46484375 38.748779296875, -34.8046875 36.287841796875, -7.20703125 36.463623046875, -9.66796875 37.869873046875, -10.37109375 39.627685546875, -9.140625 41.561279296875, -10.1953125 43.494873046875, -8.7890625 44.725341796875, -5.9765625 44.373779296875, -1.93359375 44.197998046875, -2.4609375 46.834716796875, -4.39453125 48.240966796875, -5.44921875 49.119873046875, -2.28515625 49.998779296875, -5.625 50.701904296875, -5.80078125 51.932373046875, -9.31640625 51.405029296875, -10.8984375 52.283935546875, -11.07421875 53.514404296875, -10.546875 55.272216796875, -9.31640625 55.623779296875, -7.734375 56.151123046875, -7.3828125 57.381591796875, -7.734375 59.315185546875, -7.20703125 60.369873046875, -29.35546875 60.369873046875))'''

   wkt_poly2 = 'POLYGON((-15.380859375 51.976318359375, -14.501953125 50.262451171875, -12.83203125 50.833740234375, -12.12890625 52.064208984375, -10.9423828125 50.174560546875, -11.9091796875 49.339599609375, -9.052734375 47.098388671875, -5.4052734375 46.263427734375, -5.537109375 43.978271484375, -9.4921875 44.154052734375, -15.732421875 45.340576171875, -16.34765625 48.021240234375, -15.380859375 51.976318359375))'

   wkt_line = 'LINESTRING(-4.21875 50.174560546875, -6.15234375 46.307373046875, -9.4921875 45.252685546875, -11.77734375 40.858154296875, -11.953125 35.584716796875, -14.58984375 29.783935546875, -19.3359375 24.686279296875, -18.28125 17.655029296875, -22.32421875 10.623779296875, -23.90625 3.592529296875, -26.015625 -5.899658203125, -30.234375 -13.282470703125, -36.2109375 -28.399658203125, -39.7265625 -38.243408203125, -39.7265625 -42.813720703125)'

   wkt_circle = 'POLYGON((-8.789062500000004 46.307373046875, -8.745276012599003 46.357418951702265, -8.70228101393557 46.408146450742024, -8.660088112382276 46.45954302774294, -8.618707718406231 46.51159600136871, -8.578150042000464 46.564292528326966, -8.538425090164749 46.6176196065382, -8.499542664436534 46.67156407834382, -8.461512358472557 46.72611263375259, -8.424343555681759 46.781251813724694, -8.38804542691005 46.83696801349254, -8.352626928177575 46.89324748591752, -8.318096798468911 46.95007634488196, -8.284463557576881 47.00744056871525, -8.251735504000411 47.065326003653524, -8.219920712896997 47.12371836733186, -8.18902703409029 47.182603252308276, -8.159062090133267 47.241966129618504, -8.130033274427468 47.30179235236085, -8.101947749398807 47.36206715931004, -8.07481244473033 47.42277567855936, -8.048634055652428 47.483902931190116, -8.023419041290893 47.54543383496736, -7.999173623073217 47.607353208061305, -7.975903783193553 47.66964577279316, -7.953615263136696 47.732296159404676, -7.932313562261462 47.79528890985041, -7.9120039364437975 47.85860848161179, -7.892691396779973 47.922239251531934, -7.87438070835017 47.9861655196705, -7.8570763890427715 48.050371513177375, -7.840782708439636 48.114841390184395, -7.825503686762643 48.179559243714095, -7.811243093881768 48.2445091056045, -7.79800444838492 48.30967495044907, -7.785791016709779 48.375040699550674, -7.774605812337857 48.440590224888815, -7.764451595050967 48.506307353098954, -7.7553308702502814 48.57217586946305, -7.7472458883381705 48.63817952191031, -7.740198644162942 48.70430202502711, -7.734190876526646 48.77052706407524, -7.72922406775605 48.836838299017245, -7.7252994433369 48.903219368548136, -7.722417971611544 48.96965389413231, -7.720580363540015 49.03612548404463, -7.719787072524608 49.10261773741495, -7.720038294298011 49.169114248274674, -7.721333966875008 49.23559860960477, -7.723673770567781 49.3020544173839, -7.7270571280647795 49.368465274635895, -7.731483204573167 49.434814795475454, -7.736950908024793 49.50108660915112, -7.743458889345647 49.56726436408452, -7.75100554278872 49.63333173190485, -7.759589006330196 49.69927241147771, -7.769207162128883 49.76507013292708, -7.77985763704876 49.83070866164976, -7.791537803244505 49.896171802320964, -7.804244778809883 49.96144340289026, -7.817975428488811 50.0265073585669, -7.8327263644489395 50.09134761579339, -7.848493947117543 50.155948176206486, -7.86527428607953 50.22029310058455, -7.883063241037355 50.28436651278029, -7.901856422832563 50.34815260363801, -7.9216491945287535 50.411635634894246, -7.942436672555678 50.474799943060944, -7.96421372791418 50.53762994329021, -7.986974987441709 50.600110133219644, -8.01071483513806 50.66222509679728, -8.03542741355104 50.72395950808531, -8.061106625221711 50.785298135041494, -8.087746134188837 50.846225843277466, -8.115339367552197 50.9067275997929, -8.143879517094344 50.96678847668468, -8.173359540960433 51.02639365483014, -8.203772165395698 51.085528427543466, -8.235109886540128 51.144178204204344, -8.267364972279951 51.202328513857985, -8.300529464155403 51.25996500878559, -8.334595179324364 51.317073468044484, -8.369553712581352 51.37363980097687, -8.405396438431383 51.42965005068651, -8.442114513218181 51.4850903974824, -8.479698877306213 51.539947162288534, -8.518140257316029 51.59420681001904, -8.557429168412321 51.64785595291774, -8.597555916644172 51.70088135386139, -8.638510601336883 51.753269929625745, -8.680283117534822 51.80500875411365, -8.722863158494677 51.85608506154434, -8.766240218228477 51.90648624960323, -8.810403594095801 51.95619988255134, -8.85534238944448 52.00521369429361, -8.901045516299195 52.05351559140541, -8.947501698097271 52.10109365611638, -8.994699472470984 52.14793614925099, -9.042627194075742 52.194031513124955, -9.0912730374634 52.239368374397, -9.140625000000004 52.283935546875, -9.190670904827265 52.32772203427599, -9.241398403867024 52.37071703293943, -9.29279498086794 52.412909934492724, -9.344847954493707 52.454290328468765, -9.397544481451964 52.494848004874534, -9.450871559663202 52.53457295671025, -9.50481603146882 52.57345538243847, -9.559364586877589 52.61148568840244, -9.61450376684969 52.64865449119324, -9.670219966617534 52.684952619964946, -9.72649943904252 52.72037111869742, -9.783328298006959 52.754901248406085, -9.84069252184025 52.788534489298115, -9.89857795677852 52.82126254287459, -9.956970320456863 52.85307733397801, -10.015855205433276 52.88397101278471, -10.075218082743508 52.91393595674173, -10.135044305485847 52.94296477244753, -10.195319112435033 52.97105029747619, -10.256027631684363 52.998185602144666, -10.317154884315112 53.02436399122257, -10.378685788092358 53.04957900558411, -10.440605161186305 53.07382442380178, -10.502897725918157 53.09709426368145, -10.565548112529672 53.1193827837383, -10.628540862975415 53.14068448461354, -10.691860434736789 53.160994110431204, -10.755491204656934 53.18030665009503, -10.819417472795502 53.198617338524826, -10.883623466302376 53.215921657832226, -10.948093343309397 53.23221533843537, -11.012811196839095 53.247494360112356, -11.077761058729504 53.26175495299323, -11.14292690357407 53.274993598490084, -11.208292652675674 53.28720703016522, -11.273842178013817 53.29839223453715, -11.339559306223956 53.308546451824036, -11.405427822588054 53.31766717662472, -11.47143147503531 53.32575215853683, -11.537553978152115 53.332799402712055, -11.603779017200239 53.33880717034835, -11.670090252142243 53.34377397911895, -11.736471321673141 53.3476986035381, -11.802905847257307 53.35058007526346, -11.869377437169636 53.352417683334984, -11.935869690539949 53.35321097435039, -12.00236620139968 53.35295975257699, -12.068850562729772 53.35166407999999, -12.135306370508902 53.34932427630722, -12.201717227760895 53.34594091881022, -12.268066748600456 53.341514842301834, -12.334338562276121 53.336047138850205, -12.40051631720952 53.329539157529354, -12.466583685029855 53.32199250408628, -12.532524364602706 53.313409040544805, -12.598322086052079 53.303790884746114, -12.663960614774762 53.293140409826236, -12.72942375544596 53.2814602436305, -12.79469535601526 53.26875326806512, -12.859759311691901 53.25502261838619, -12.92459956891839 53.24027168242606, -12.989200129331486 53.22450409975746, -13.053545053709545 53.20772376079547, -13.11761846590529 53.189934805837645, -13.181404556763011 53.171141624042434, -13.244887588019246 53.151348852346246, -13.308051896185942 53.13056137431932, -13.370881896415213 53.10878431896082, -13.433362086344642 53.08602305943329, -13.49547704992228 53.06228321173694, -13.55721146121031 53.03757063332396, -13.618550088166495 53.01189142165329, -13.679477796402468 52.98525191268617, -13.739979552917898 52.957658679322805, -13.800040429809675 52.92911852978066, -13.859645607955137 52.89963850591457, -13.918780380668466 52.8692258814793, -13.977430157329346 52.83788816033487, -14.035580466982983 52.80563307459505, -14.093216961910592 52.7724685827196, -14.150325421169484 52.73840286755063, -14.206891754101868 52.70344433429365, -14.262902003811512 52.66760160844362, -14.318342350607402 52.63088353365682, -14.373199115413536 52.59329916956879, -14.427458763144038 52.55485778955897, -14.481107906042737 52.51556887846267, -14.534133306986389 52.475442130230824, -14.586521882750748 52.43448744553812, -14.63826070723865 52.39271492934018, -14.689337014669341 52.350134888380325, -14.73973820272823 52.306757828646525, -14.789451835676335 52.2625944527792, -14.838465647418609 52.21765565743052, -14.886767544530407 52.1719525305758, -14.93434560924138 52.12549634877773, -14.981188102375985 52.078298574404016, -15.027283466249958 52.03037085279926, -15.072620327522005 51.9817250094116, -15.117187499999996 51.932373046875, -15.160973987400997 51.882327142047735, -15.20396898606443 51.831599643007976, -15.246161887617724 51.78020306600706, -15.287542281593769 51.72815009238129, -15.328099957999536 51.675453565423034, -15.36782490983525 51.6221264872118, -15.406707335563466 51.56818201540618, -15.444737641527443 51.51363345999741, -15.481906444318241 51.458494280025306, -15.51820457308995 51.40277808025746, -15.553623071822425 51.34649860783248, -15.588153201531089 51.289669748868036, -15.621786442423119 51.23230552503475, -15.65451449599959 51.174420090096476, -15.686329287103003 51.11602772641814, -15.71722296590971 51.057142841441724, -15.747187909866733 50.997779964131496, -15.776216725572532 50.93795374138915, -15.804302250601193 50.87767893443996, -15.83143755526967 50.81697041519064, -15.857615944347572 50.755843162559884, -15.882830958709107 50.69431225878264, -15.907076376926783 50.632392885688695, -15.930346216806448 50.57010032095684, -15.952634736863304 50.507449934345324, -15.973936437738537 50.44445718389959, -15.994246063556202 50.38113761213821, -16.013558603220027 50.317506842218066, -16.03186929164983 50.2535805740795, -16.04917361095723 50.18937458057262, -16.065467291560367 50.124904703565605, -16.080746313237356 50.060186850035905, -16.095006906118233 49.9952369881455, -16.10824555161508 49.93007114330093, -16.12045898329022 49.864705394199326, -16.131644187662143 49.799155868861185, -16.141798404949032 49.733438740651046, -16.150919129749717 49.66757022428695, -16.15900411166183 49.60156657183969, -16.166051355837055 49.53544406872289, -16.172059123473353 49.46921902967476, -16.17702593224395 49.402907794732755, -16.1809505566631 49.33652672520186, -16.183832028388455 49.27009219961769, -16.185669636459984 49.20362060970537, -16.186462927475393 49.13712835633505, -16.18621170570199 49.070631845475326, -16.184916033124992 49.00414748414523, -16.182576229432218 48.9376916763661, -16.17919287193522 48.871280819114105, -16.174766795426834 48.804931298274546, -16.169299091975205 48.73865948459888, -16.162791110654354 48.67248172966548, -16.155244457211282 48.60641436184515, -16.146660993669805 48.54047368227229, -16.137042837871117 48.47467596082292, -16.12639236295124 48.409037432100234, -16.114712196755494 48.343574291429036, -16.10200522119012 48.27830269085974, -16.08827457151119 48.2132387351831, -16.073523635551062 48.14839847795661, -16.057756052882457 48.083797917543514, -16.040975713920467 48.01945299316545, -16.023186758962645 47.955379580969705, -16.004393577167434 47.89159349011199, -15.984600805471246 47.828110458855754, -15.963813327444322 47.764946150689056, -15.94203627208582 47.70211615045979, -15.919275012558291 47.639635960530356, -15.89553516486194 47.57752099695272, -15.87082258644896 47.51578658566469, -15.845143374778287 47.4544479587085, -15.818503865811161 47.39352025047253, -15.790910632447803 47.3330184939571, -15.762370482905656 47.27295761706532, -15.732890459039565 47.21335243891986, -15.702477834604302 47.154217666206534, -15.671140113459872 47.095567889545656, -15.638885027720049 47.037417579892015, -15.605720535844597 46.97978108496441, -15.571654820675636 46.922672625705516, -15.536696287418648 46.86610629277313, -15.500853561568615 46.81009604306348, -15.464135486781819 46.7546556962676, -15.426551122693786 46.69979893146146, -15.38810974268397 46.64553928373096, -15.348820831587677 46.59189014083226, -15.308694083355828 46.53886473988861, -15.267739398663117 46.486476164124255, -15.225966882465178 46.43473733963635, -15.183386841505323 46.38366103220566, -15.140009781771523 46.33325984414677, -15.0958464059042 46.28354621119866, -15.05090761055552 46.23453239945639, -15.005204483700801 46.18623050234459, -14.958748301902729 46.13865243763362, -14.911550527529016 46.09180994449901, -14.863622805924257 46.045714580625045, -14.8149769625366 46.000377719353, -14.765624999999996 45.955810546875, -14.715579095172735 45.91202405947401, -14.664851596132976 45.86902906081057, -14.61345501913206 45.826836159257276, -14.561402045506295 45.785455765281235, -14.508705518548034 45.744898088875466, -14.455378440336796 45.70517313703975, -14.40143396853118 45.66629071131153, -14.346885413122408 45.62826040534756, -14.291746233150308 45.59109160255676, -14.236030033382466 45.554793473785054, -14.17975056095748 45.51937497505258, -14.122921701993041 45.484844845343915, -14.06555747815975 45.451211604451885, -14.00767204322148 45.418483550875415, -13.949279679543137 45.38666875977199, -13.890394794566724 45.35577508096529, -13.831031917256492 45.32581013700827, -13.771205694514151 45.29678132130247, -13.710930887564965 45.26869579627381, -13.650222368315637 45.24156049160533, -13.589095115684888 45.21538210252743, -13.527564211907642 45.19016708816589, -13.465644838813695 45.16592166994822, -13.403352274081843 45.14265183006855, -13.340701887470328 45.1203633100117, -13.277709137024587 45.09906160913646, -13.214389565263211 45.078751983318796, -13.15075879534307 45.05943944365497, -13.086832527204498 45.041128755225174, -13.022626533697627 45.023824435917774, -12.958156656690605 45.00753075531463, -12.893438803160905 44.992251733637644, -12.8284889412705 44.97799114075677, -12.76332309642593 44.964752495259916, -12.697957347324328 44.95253906358478, -12.632407821986185 44.94135385921285, -12.56669069377605 44.931199641925964, -12.500822177411948 44.92207891712528, -12.434818524964696 44.91399393521317, -12.368696021847887 44.906946691037945, -12.302470982799766 44.90093892340165, -12.236159747857759 44.89597211463105, -12.169778678326859 44.8920474902119, -12.103344152742697 44.88916601848654, -12.036872562830364 44.887328410415016, -11.970380309460053 44.88653511939961, -11.903883798600322 44.88678634117301, -11.837399437270232 44.88808201375001, -11.7709436294911 44.89042181744278, -11.704532772239109 44.89380517493978, -11.638183251399546 44.898231251448166, -11.571911437723879 44.903698954899795, -11.505733682790483 44.910206936220646, -11.439666314970143 44.91775358966372, -11.373725635397296 44.926337053205195, -11.30792791394792 44.935955209003886, -11.242289385225241 44.94660568392376, -11.17682624455404 44.9582858501195, -11.111554643984743 44.97099282568488, -11.0464906883081 44.98472347536381, -10.98165043108161 44.99947441132394, -10.917049870668514 45.01524199399254, -10.852704946290451 45.03202233295453, -10.788631534094712 45.049811287912355, -10.724845443236987 45.068604469707566, -10.661362411980758 45.088397241403754, -10.598198103814058 45.10918471943068, -10.535368103584792 45.13096177478918, -10.472887913655358 45.15372303431671, -10.41077295007772 45.17746288201306, -10.34903853878969 45.20217546042604, -10.287699911833505 45.22785467209671, -10.226772203597534 45.25449418106383, -10.166270447082098 45.282087414427195, -10.106209570190327 45.31062756396934, -10.046604392044863 45.34010758783543, -9.987469619331538 45.3705202122707, -9.928819842670656 45.40185793341513, -9.870669533017018 45.43411301915495, -9.813033038089408 45.4672775110304, -9.755924578830516 45.50134322619936, -9.699358245898132 45.53630175945635, -9.643347996188488 45.57214448530638, -9.587907649392598 45.60886256009318, -9.533050884586462 45.64644692418121, -9.478791236855963 45.68488830419103, -9.425142093957263 45.72417721528732, -9.372116693013611 45.764303963519176, -9.319728117249253 45.80525864821188, -9.26798929276135 45.84703116440982, -9.21691298533066 45.889611205369675, -9.16651179727177 45.932988265103475, -9.116798164323665 45.9771516409708, -9.067784352581393 46.02209043631948, -9.019482455469594 46.06779356317419, -8.971904390758619 46.11424974497227, -8.925061897624015 46.161447519345984, -8.878966533750042 46.20937524095074, -8.833629672477995 46.2580210843384, -8.789062500000004 46.307373046875))'
   jad_test = 'POLYGON((-8.0859375 48.328857421875, -8.19580078125 48.438720703125, -8.32763671875 48.526611328125, -8.37158203125 48.724365234375, -8.349609375 48.966064453125, -8.2177734375 49.229736328125, -7.97607421875 49.295654296875, -7.734375 49.295654296875, -7.49267578125 49.185791015625, -7.3828125 49.273681640625, -7.31689453125 49.515380859375, -7.31689453125 49.757080078125, -7.294921875 50.086669921875, -7.31689453125 50.372314453125, -7.2509765625 50.789794921875, -7.20703125 51.361083984375, -6.8994140625 51.668701171875, -6.61376953125 51.690673828125, -6.43798828125 51.514892578125, -6.30615234375 51.251220703125, -6.1962890625 50.943603515625, -6.2841796875 50.614013671875, -6.21826171875 50.218505859375, -6.26220703125 49.844970703125, -6.2841796875 49.515380859375, -6.2841796875 49.207763671875, -6.21826171875 49.075927734375, -6.1083984375 49.075927734375, -5.9326171875 49.207763671875, -5.77880859375 49.361572265625, -5.60302734375 49.295654296875, -5.4052734375 49.031982421875, -5.3173828125 48.680419921875, -5.3173828125 48.394775390625, -5.4052734375 48.109130859375, -5.8447265625 48.153076171875, -6.591796875 48.065185546875, -7.294921875 48.065185546875, -7.91015625 48.197021484375, -8.0859375 48.328857421875))'
   masked_chl = create_mask(jad_test, 'chlor_a', poly_type="polygon")
   plt.imshow(masked_chl)
   plt.show()