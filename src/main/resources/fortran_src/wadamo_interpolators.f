      subroutine linint2index(x,xtab,y,din,dtab)
      implicit none
C     returns the broken index of a 1-d table
C     in python notation (zero indexed)
c     automatic clipping
CF2PY INTENT(IN) :: x,xtab
CF2PY INTENT(OUT) :: y
CF2PY INTENT(HIDE) :: dtab
CF2PY DOUBLE :: xtab(dtab)
CF2PY DOUBLE :: x(din)
      integer i,j
      INTEGER din, dtab
      DOUBLE PRECISION x(din),xtab(dtab),y(din)
      
      do 100 i = 1, din
        if (x(i) .le. xtab(1)) then 
          y(i) = 0.d0
          goto 100
        endif  
        if (x(i) .ge. xtab(dtab)) then 
          y(i) = dble(dtab) -1.d0
          goto 100
        endif  
        do 200 j = 2, dtab-1
          if (x(i) .lt. xtab(j)) goto 300
 200    continue   
 300     y(i)=dble(j-1)+(x(i)-xtab(j-1))/(xtab(j)-xtab(j-1))-1.d0
 100  continue
      end      
      


      SUBROUTINE interpol_6to1(xx,lut,out,d0,d1,d2,d3,d4,d5)

C     input is index
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d0,d1,d2,d3,d4,d5
CF2PY DOUBLE :: lut(d0,d1,d2,d3,d4,d5)
CF2PY DOUBLE :: out(d0)
      integer i
      INTEGER d0,    d1,    d2,    d3,    d4,    d5
      INTEGER j0,    j1,    j2,    j3,    j4,    j5
      INTEGER        kk(5,2),dd(5)
      DOUBLE PRECISION lut(d0,d1,d2,d3,d4,d5)
      DOUBLE PRECISION out(d0)
      DOUBLE PRECISION ww(5,2),xx(5)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
       
      !positions
      do i=1,5
        kk(i,1) = max(0,idint(xx(i)))
        kk(i,1) = min(dd(i)-1,kk(i,1))
        kk(i,2) = min(dd(i)-1,kk(i,1)+1)
!         kk(i,1) = idint(xx(i))
!         kk(i,2) = kk(i,1)+1
      enddo  
      !weights
      do i=1,5
!         ww(i,1)=1.d0-(xx(i)-dble(kk(i,1)))
        ww(i,2)=(xx(i)-kk(i,1))
        ww(i,1)=1.d0-ww(i,2)
      enddo
      !fortran style 
      do i=1,5
        kk(i,1) = kk(i,1)+1
        kk(i,2) = kk(i,2)+1
      enddo  
      

      !define output
      do j0 = 1, d0
         out(j0) = 0.d0
      enddo

      !doit   
      DO 10 j5 = 1, 2
      DO 20 j4 = 1, 2
      DO 30 j3 = 1, 2
      DO 40 j2 = 1, 2
      DO 50 j1 = 1, 2
      wgt=ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)*ww(5,j5)
        DO 01 j0 = 1, d0
        out(j0) = out(j0)
     %       +lut(j0,kk(1,j1),kk(2,j2),kk(3,j3),kk(4,j4),kk(5,j5))
     %       *wgt
 01     CONTINUE
 50   CONTINUE
 40   CONTINUE
 30   CONTINUE
 20   CONTINUE
 10   CONTINUE
      END
      
      
      
      SUBROUTINE interpol_5to1(xx,lut,out,d0,d1,d2,d3,d4)
C
C     input is index
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d0,d1,d2,d3,d4
CF2PY DOUBLE :: lut(d0,d1,d2,d3,d4)
CF2PY DOUBLE :: out(d0)
      integer i
      INTEGER d0,    d1,    d2,    d3,    d4
      INTEGER j0,    j1,    j2,    j3,    j4
      INTEGER        kk(4,2),dd(4)
      DOUBLE PRECISION lut(d1,d0,d2,d3,d4)
      DOUBLE PRECISION out(d0)
      DOUBLE PRECISION ww(4,2),xx(4)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
       
      !positions
      do i=1,4
        kk(i,1) = max(0,idint(xx(i)))
        kk(i,1) = min(dd(i)-1,kk(i,1))
        kk(i,2) = min(dd(i)-1,kk(i,1)+1)
      enddo  
      !weights
      do i=1,4
!         ww(i,1)=1.d0-(xx(i)-dble(kk(i,1)))
        ww(i,2)=(xx(i)-kk(i,1))
        ww(i,1)=1.d0-ww(i,2)
      enddo
      !fortran style 
      do i=1,4
        kk(i,1) = kk(i,1)+1
        kk(i,2) = kk(i,2)+1
      enddo  
      

      !define output
      do j0 = 1, d0
         out(j0) = 0.d0
      enddo

      !doit   
      DO 10 j4 = 1, 2
      DO 20 j3 = 1, 2
      DO 30 j2 = 1, 2
      DO 40 j1 = 1, 2
      wgt=ww(1,j1)*ww(2,j2)*ww(3,j3)*ww(4,j4)
        DO 01 j0 = 1, d0
        out(j0) = out(j0)
     %       +lut(kk(1,j1),j0,kk(2,j2),kk(3,j3),kk(4,j4))
     %       *wgt
 01     CONTINUE
 40   CONTINUE
 30   CONTINUE
 20   CONTINUE
 10   CONTINUE
      END


      SUBROUTINE interpol_6(xx,lut,out,d1,d2,d3,d4,d5,d6,din)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6,din
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6)
CF2PY DOUBLE :: out(din)
CF2PY DOUBLE :: xx(6,din)
      integer i
      INTEGER d1, d2, d3, d4, d5, d6, din
      INTEGER j1, j2, j3, j4, j5, j6, jin
      INTEGER        kk(6,2),dd(6)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6)
      DOUBLE PRECISION out(din)
      DOUBLE PRECISION ww(6,2),xx(6,din)
      DOUBLE PRECISION wgt
      
      
      !shape of LUT
      dd(1)=d1
      dd(2)=d2
      dd(3)=d3
      dd(4)=d4
      dd(5)=d5
      dd(6)=d6
      
      do 1234 jin=1,din
            !positions
            do i=1,6
              kk(i,1) = max(0,idint(xx(i,jin)))
              kk(i,1) = min(dd(i)-1,kk(i,1))
              kk(i,2) = min(dd(i)-1,kk(i,1)+1)
            enddo  
            !weights
            do i=1,6
              ww(i,2)=(xx(i,jin)-kk(i,1))
              ww(i,1)=1.d0-ww(i,2)
            enddo
            !fortran style 
            do i=1,6
              kk(i,1) = kk(i,1)+1
              kk(i,2) = kk(i,2)+1
            enddo  
            
            !define output
            out(jin) = 0.d0
            
            !doit   
            DO 10 j6 = 1, 2
            DO 20 j5 = 1, 2
            DO 30 j4 = 1, 2
            DO 40 j3 = 1, 2
            DO 50 j2 = 1, 2
            DO 60 j1 = 1, 2
            wgt = ww(1,j1)*ww(2,j2)*ww(3,j3)
     %           *ww(4,j4)*ww(5,j5)*ww(6,j6)
            out(jin) = out(jin) + lut(kk(1,j1),kk(2,j2),kk(3,j3)
     %      ,kk(4,j4),kk(5,j5),kk(6,j6))
     %      *wgt
   60       CONTINUE
   50       CONTINUE
   40       CONTINUE
   30       CONTINUE
   20       CONTINUE
   10       CONTINUE
 1234 enddo 
      end

      
      SUBROUTINE interpol_6_full(xx,lut,a1,a2,a3,a4,a5,a6,out
     %                                 ,d1,d2,d3,d4,d5,d6,din)
      implicit none
C
C     input is real space
CF2PY INTENT(IN) :: xx,lut,a1,a2,a3,a4,a5,a6
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,d2,d3,d4,d5,d6,din
CF2PY DOUBLE :: lut(d1,d2,d3,d4,d5,d6)
CF2PY DOUBLE :: a1(d1),a2(d2),a3(d3),a4(d4),a5(d5),a6(d6)
CF2PY DOUBLE :: out(din)
CF2PY DOUBLE :: xx(6,din)
      integer i
      INTEGER d1, d2, d3, d4, d5, d6, din
      DOUBLE PRECISION a1(d1),a2(d2),a3(d3),a4(d4),a5(d5),a6(d6)
      DOUBLE PRECISION lut(d1,d2,d3,d4,d5,d6)
      DOUBLE PRECISION out(din)
      DOUBLE PRECISION xx(6,din),oo(6,din)
      DOUBLE PRECISION dum(1)
      do i = 1, din
        call linint2index(xx(1,i),a1,dum,1,d1)
        oo(1,i)= dum(1)
        call linint2index(xx(2,i),a2,dum,1,d2)
        oo(2,i)= dum(1)
        call linint2index(xx(3,i),a3,dum,1,d3)
        oo(3,i)= dum(1)
        call linint2index(xx(4,i),a4,dum,1,d4)
        oo(4,i)= dum(1)
        call linint2index(xx(5,i),a5,dum,1,d5)
        oo(5,i)= dum(1)
        call linint2index(xx(6,i),a6,dum,1,d6)
        oo(6,i)= dum(1)
      enddo 
      call interpol_6(oo,lut,out,d1,d2,d3,d4,d5,d6,din)      
      end
 

      SUBROUTINE interpol_1(xx,lut,out,d1,din)
      implicit none

C input is index, NO LIMIT CHECKS      
C
CF2PY INTENT(IN) :: lut, xx
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: d1,din
CF2PY DOUBLE :: lut(d1)
CF2PY DOUBLE :: out(din)
CF2PY DOUBLE :: xx(din)
      INTEGER d1, din
      INTEGER j1, jin
      INTEGER  kk(2)
      DOUBLE PRECISION lut(d1)
      DOUBLE PRECISION out(din),xx(din)
      DOUBLE PRECISION ww(2)
           
      do 1234 jin=1,din
            !positions
              kk(1) = max(0,idint(xx(jin)))
              kk(2) = min(d1-1,kk(1)+1)
            !weights
              ww(2)=(xx(jin)-kk(1))
              ww(1)=1.d0-ww(2)
            !fortran style 
              kk(1) = kk(1)+1
              kk(2) = kk(2)+1            
            !define output
            out(jin) = 0.d0
            
            !doit   
            DO 10 j1 = 1, 2
              out(jin) = out(jin) + lut(kk(j1))*ww(j1)
   10       CONTINUE
 1234 enddo 
      end

      
      SUBROUTINE interpol_1_full(xx,yref,xref,yy,d1,din)
      implicit none

C input is real, implicit cliping      
C
CF2PY INTENT(IN) :: yref,xref, xx
CF2PY INTENT(OUT) :: yy
CF2PY INTENT(HIDE) :: d1,din
CF2PY DOUBLE :: yref(d1),xref(d1)
CF2PY DOUBLE :: yy(din)
CF2PY DOUBLE :: xx(din)
      INTEGER d1, din
      DOUBLE PRECISION yref(d1),xref(d1)
      DOUBLE PRECISION yy(din),xx(din),oo(din)
      call linint2index(xx,xref,oo,din,d1)
      call interpol_1(oo,yref,yy,d1,din)      
      
      end

