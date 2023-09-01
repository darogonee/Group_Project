import polyline
# print(polyline.decode("hxudGu|ob[PgKTgEl@uEl@wCd@oAj@eAhAgAGBo@z@MHUd@[d@i@xAMd@Eb@UvAIjAIf@A`@G`@Cv@MvAG`D@XIfA@~@GlBCfCGnCAnGC|@?t@E^@??F@ABXDlHIxBCJ?@C?BDAFO?@G?@AA@AC@B?AB@AE@D@CEBCC@@?A?@A?A?HAB@E?DSBECF?C?BFOiAOy@Jl@ThCAC?SQkBGa@CAHXLxA?HA?@@A_@WoBE{@@a@Fk@E]Sy@Gu@?w@BcAIkB?iCIiACeC@uBFa@X_@@SAoB@cCLaDDmCD_@XgB?yAFa@tAqFJ[Zg@XcANWTMLChBRfAANEp@g@vAq@`@k@HQBQA]QoAGy@?^TxABf@CVITU\\WRuAr@OD]\\g@ACBD@E?@ILBMDRBZGjAw@p@[RQV]Pa@?e@UaBA]NcBJk@A]Sm@KKg@Q}@OSUQ_AEm@BcDO{@KYOqAIQ@GIW?}@C]Ki@WaBj@{E@_@Cm@Ba@n@}CFs@FqB`@_CPaGL_AJuBAYHUABB?DE`@eBRyBVgBBmAn@yBf@{@h@oCf@gADUBo@DUPq@\\u@Rw@Hs@FaBF]Rq@J}@@RET[bAANMzBIn@GV}@lCEVCl@K^OXK\\U`ASlAIRc@r@m@jBs@dAk@l@OXu@zBB@@D@AAA?D@FKBICXDf@E\\BPCTM@??DKx@i@rBE|AQjBUjFc@jDG|AYpBWxAAbBg@lFDPFFA?@LARNd@D\\@`BTp@FZBf@Rl@H^@^GrCBZVpADFJDt@Jl@VRVNj@@XOr@OrARfCCd@GR_@h@QJGAEH}@b@u@h@sA@eBSYFOJKR[hAa@|@yAhGCV?jA[~BG|CKlC@h@KrBBz@C_BBu@Am@F{@EfA?lAEpCYrAAz@BbEHz@BvCFlBEfCB^XdA@L?TGj@@n@NfAHnA\\DF?DE@CC@?GCA@@CAF@?y@D`@AFD@EAAZGDe@CEKG?S`@GVOZg@z@a@f@IP@@A?@ED?FSIgA?e@b@aAb@cB\\yAJ_A?WWcAGm@BkBGwB@sBImACyF@YHYLWFc@AuABkCLkD@}AFqAXiB@s@AQAz@YbBGfBAhBO|CAnC@rAEb@Ud@E\\@xEFnA"))

# import gmplot package 
import gmplot 
 
latitude_list = [ 30.3358376, 30.307977, 30.3216419 ] 
longitude_list = [ 77.8701919, 78.048457, 78.0413095 ] 
 
gmap3 = gmplot.GoogleMapPlotter(30.3164945, 
								78.03219179999999, 13) 
 
# scatter method of map object 
# scatter points on the google map 
gmap3.scatter( latitude_list, longitude_list, 
							size = 40, marker = False ) 
 
# Plot method Draw a line in 
# between given coordinates 
gmap3.plot(latitude_list, longitude_list, 
		'cornflowerblue', edge_width = 2.5) 
 
gmap3.draw( "C:\\Users\\user\\Desktop\\map13.html" ) 