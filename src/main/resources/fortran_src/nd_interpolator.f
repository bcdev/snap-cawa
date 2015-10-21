      subroutine linint2index(x,xtab,y,dtab)
      implicit none
C     returns the broken index of a 1-d table
C     in python notation (zero indexed)
c     automatic clipping
CF2PY INTENT(IN) :: x,xtab
CF2PY INTENT(OUT) :: y
CF2PY INTENT(HIDE) :: dtab
CF2PY DOUBLE :: xtab(dtab)
CF2PY DOUBLE :: x,y
CF2PY INTEGER :: dtab
      INTEGER j
      INTEGER  dtab
      DOUBLE PRECISION x,xtab(dtab),y
      
        if (x .le. xtab(1)) then 
          y = 0.d0
        else if (x .ge. xtab(dtab)) then 
          y = dble(dtab) -1.d0
        else   
            do j = 2, dtab-1
                if (x .lt. xtab(j)) exit
            enddo   
            y=dble(j-1)+(x-xtab(j-1))/(xtab(j)-xtab(j-1))-1.d0
        endif
      end

      
      subroutine linint2index_vector(x,xtab,y,din,dtab)
      implicit none
C     returns the broken index of a 1-d table
C     in python notation (zero indexed)
c     automatic clipping
CF2PY INTENT(IN) :: x,xtab
CF2PY INTENT(OUT) :: y
CF2PY INTENT(HIDE) :: dtab
CF2PY DOUBLE :: xtab(dtab)
CF2PY DOUBLE :: x(din),y(din)
      INTEGER i
      INTEGER din, dtab
      DOUBLE PRECISION x(din),xtab(dtab),y(din)      
      do i = 1, din
        call linint2index(x(i),xtab,y(i),dtab)
      enddo
      end
    
      
      subroutine en_cl(xx,kk,ww,dd,d)
      implicit none
!     returns 
!     1.: lower index and lower weight 
!     2.: upper index and upper weight
!     k: place
!     w: weight
!     d: rank
      INTEGER i,d
      INTEGER kk(d,2),dd(d)
      double precision xx(d),ww(d,2)
        do i=1,d
            kk(i,1) = max(0,idint(xx(i)))
            kk(i,1) = min(dd(i)-1,kk(i,1))
            kk(i,2) = min(dd(i)-1,kk(i,1)+1)
        enddo  
        !weights
        do i=1,d
            ww(i,2)=(xx(i)-kk(i,1))
            ww(i,1)=1.d0-ww(i,2)
        enddo
        !fortran style 
        do i=1,d
            kk(i,1) = kk(i,1)+1
            kk(i,2) = kk(i,2)+1
        enddo        
      end
      
            
            
      SUBROUTINE indexto1(jj,dd,rank,out)
      implicit none
      INTEGER rank
      INTEGER*8 i,mul,out
      INTEGER jj(rank)
      INTEGER*8 dd(rank)
      out=jj(rank)-1   
      mul=1
      do 10 i=1,rank-1 
        mul=mul*dd(rank-i+1)
        out=out+mul*(jj(rank-i)-1)
10    continue
      out=out+1
      end
      
      subroutine permute_two(n,b,out)
      implicit none
      integer n,b,i
      integer out(b)
      logical lll
      do i=0,b-1
      !no implicit conversion in fortran :-(
        lll = btest(n-1,i)
        if ( lll ) then
            out(b-i)= 2
        else 
            out(b-i)= 1
        endif    
      enddo
      end

!       subroutine permute_two(n,b,out)
!       implicit none
!       integer n,b,i
!       integer out(b)
!       do i=0,b-1
!         out(b-i) = btest(n-1,i)
!       enddo
!         out=out+1
!       end
      
        
      
      SUBROUTINE interpol_n(xx,lut,dd,out,si,di)
      implicit none

C     input is index
C
CF2PY INTENT(IN) :: lut,xx,dd,si
CF2PY INTENT(OUT) :: out
CF2PY INTENT(HIDE) :: si,di
CF2PY DOUBLE :: lut(si)
CF2PY DOUBLE :: out
CF2PY DOUBLE :: xx(di)
CF2PY INTEGER :: si,di
CF2PY INTEGER*8 :: dd(di)
!       INTEGER j1, j2, j3, j4, j5, j6, j7, j8, i,j, di
      INTEGER i,j, di
      INTEGER kk(di,2),dl(di),nd_idx(di),jj(di)
      INTEGER*8 dd(di),idx,si
      DOUBLE PRECISION lut(si)
      DOUBLE PRECISION out,xx(di)
      DOUBLE PRECISION ww(di,2)
      DOUBLE PRECISION wgt
      
      
      do i=1,di
         dl(i)=long(dd(i))
      enddo      
      call en_cl(xx,kk,ww,dl,di)

      out = 0.d0        
      do i=1,2**di
        call permute_two(i,di,jj)
        wgt=1.d0 
        do j=1,di
                nd_idx(j)=kk(j,jj(j))
                wgt = wgt*ww(j,jj(j))
        enddo
        call indexto1(nd_idx,dd,di,idx) 
        out = out + lut(idx)*wgt 
      enddo      
      end
      

       